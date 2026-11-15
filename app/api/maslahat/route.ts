import Anthropic from "@anthropic-ai/sdk";
import { getContent } from "@/lib/data";
import { buildSystemPrompt } from "@/lib/prompt";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const MAX_QUESTION = 2000;
const MAX_HISTORY = 5;
/** Bitta IP manzildan 10 daqiqada ko‘pi bilan shuncha savol. */
const LIMIT = 6;
const WINDOW_MS = 10 * 60 * 1000;
const hits = new Map<string, number[]>();

function allowed(ip: string) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (list.length >= LIMIT) {
    hits.set(ip, list);
    return false;
  }
  list.push(now);
  hits.set(ip, list);
  if (hits.size > 5000) for (const [k, v] of hits) if (!v.some((t) => now - t < WINDOW_MS)) hits.delete(k);
  return true;
}

/** Bo‘lim yoqilganmi: sahifa formani ko‘rsatishdan oldin shuni so‘raydi. */
export async function GET() {
  return Response.json({ enabled: Boolean(process.env.ANTHROPIC_API_KEY) });
}

export async function POST(req: Request) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return Response.json({ error: "not_configured" }, { status: 503 });

  const ip =
    req.headers.get("x-forwarded-for")?.split(",")[0].trim() || req.headers.get("x-real-ip") || "anon";
  if (!allowed(ip)) return Response.json({ error: "rate_limited" }, { status: 429 });

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return Response.json({ error: "bad_request" }, { status: 400 });
  }
  const { question, history } = (body || {}) as { question?: unknown; history?: unknown };
  if (typeof question !== "string" || question.trim().length < 3 || question.length > MAX_QUESTION) {
    return Response.json({ error: "bad_request" }, { status: 400 });
  }

  const messages: Anthropic.MessageParam[] = [];
  if (Array.isArray(history)) {
    for (const p of history.slice(-MAX_HISTORY)) {
      const q = (p as { q?: unknown })?.q;
      const a = (p as { a?: unknown })?.a;
      if (typeof q === "string" && typeof a === "string" && q.trim() && a.trim()) {
        messages.push({ role: "user", content: q.slice(0, MAX_QUESTION) });
        messages.push({ role: "assistant", content: a.slice(0, 6000) });
      }
    }
  }
  messages.push({ role: "user", content: question.trim() });

  const system = buildSystemPrompt(await getContent());
  const client = new Anthropic({ apiKey });
  const stream = client.messages.stream({
    model: process.env.ANTHROPIC_MODEL || "claude-sonnet-5-5",
    max_tokens: 900,
    system: [{ type: "text", text: system, cache_control: { type: "ephemeral" } }],
    messages,
  });

  const encoder = new TextEncoder();
  let closed = false;
  const out = new ReadableStream<Uint8Array>({
    start(controller) {
      stream.on("text", (delta) => {
        if (!closed) controller.enqueue(encoder.encode(delta));
      });
      stream.on("end", () => {
        if (!closed) {
          closed = true;
          controller.close();
        }
      });
      stream.on("error", (err) => {
        console.error("[maslahat]", err);
        if (!closed) {
          closed = true;
          controller.error(err);
        }
      });
    },
    cancel() {
      closed = true;
      stream.abort();
    },
  });

  return new Response(out, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Accel-Buffering": "no",
    },
  });
}
