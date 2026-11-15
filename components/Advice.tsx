"use client";

import { useEffect, useRef, useState } from "react";

type Pair = { q: string; a: string; ok: boolean; err?: string; note?: string };

const MESSAGES: Record<number, string> = {
  429: "So‘rovlar ko‘payib ketdi. Bir necha daqiqadan keyin qayta yuborib ko‘ring.",
  400: "Savol juda qisqa yoki juda uzun. Uni 2000 belgigacha, aniq qilib yozing.",
};

/** Sun’iy intellekt bilan savol-javob: javob server orqali oqim tarzida keladi. */
export default function Advice({ examples }: { examples: string[] }) {
  const [enabled, setEnabled] = useState<boolean | null>(null);
  const [pairs, setPairs] = useState<Pair[]>([]);
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const ctl = useRef<AbortController | null>(null);

  useEffect(() => {
    fetch("/api/maslahat")
      .then((r) => r.json())
      .then((d) => setEnabled(Boolean(d.enabled)))
      .catch(() => setEnabled(false));
  }, []);

  const patchLast = (p: Partial<Pair>) => setPairs((all) => all.map((x, i) => (i === all.length - 1 ? { ...x, ...p } : x)));

  async function ask(raw: string) {
    const question = raw.trim();
    if (busy || !question) return;
    const history = pairs.filter((p) => p.ok).slice(-5).map(({ q, a }) => ({ q, a }));
    setPairs((all) => [...all, { q: question, a: "", ok: false }]);
    setText("");
    setBusy(true);
    ctl.current = new AbortController();
    let acc = "";
    try {
      const res = await fetch("/api/maslahat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, history }),
        signal: ctl.current.signal,
      });
      if (res.status === 503) {
        setPairs((all) => all.slice(0, -1));
        setEnabled(false);
        return;
      }
      if (!res.ok || !res.body) {
        patchLast({ err: MESSAGES[res.status] || "Aloqa uzildi. Savolni qayta yuborib ko‘ring." });
        return;
      }
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        acc += dec.decode(value, { stream: true });
        patchLast({ a: acc });
      }
      if (acc.trim()) patchLast({ a: acc, ok: true });
      else patchLast({ err: "Javob chiqmadi. Savolni qisqaroq va aniqroq yozib ko‘ring." });
    } catch (e) {
      const stopped = (e as Error)?.name === "AbortError";
      if (acc.trim()) patchLast({ a: acc, ok: true, note: stopped ? "Javob to‘xtatildi." : "Javob uzilib qoldi. Qayta yuborib ko‘ring." });
      else if (stopped) setPairs((all) => all.slice(0, -1));
      else patchLast({ err: "Aloqa uzildi. Savolni qayta yuborib ko‘ring." });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="chat">
      <div className="thread" aria-live="polite">
        {pairs.map((p, i) => (
          <div key={i} className="pair">
            <div className="msg q">
              <span className="who">Savol</span>
              <div className="txt">{p.q}</div>
            </div>
            <div className={"msg a" + (p.err ? " err" : "")}>
              <span className="who">Javob · sun’iy intellekt</span>
              <div className="txt">{p.a || p.err || "O‘ylayapti…"}</div>
              {p.note && <span className="foot">{p.note}</span>}
            </div>
          </div>
        ))}
      </div>

      {enabled === false ? (
        <div className="notice">
          Sun’iy intellekt maslahati hozircha yoqilmagan. Bosh sahifadagi qidiruv orqali tayyor maslahatlardan
          foydalaning.
        </div>
      ) : (
        <>
          {pairs.length === 0 && (
            <div className="examples">
              {examples.map((t) => (
                <button key={t} type="button" className="term" onClick={() => setText(t)}>
                  {t}
                </button>
              ))}
            </div>
          )}
          <form
            className="ask"
            onSubmit={(e) => {
              e.preventDefault();
              ask(text);
            }}
          >
            <textarea
              id="ask"
              rows={3}
              maxLength={2000}
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
                  e.preventDefault();
                  ask(text);
                }
              }}
              placeholder="Masalan: jarima qarorini pochta orqali kech oldim, chegirma bilan to‘lay olamanmi?"
              aria-label="Savolingiz"
            />
            <div className="askrow">
              <span className="hintkey">Enter — yuborish, Shift+Enter — yangi qator</span>
              {busy && (
                <button className="btn ghost" type="button" onClick={() => ctl.current?.abort()}>
                  To‘xtatish
                </button>
              )}
              <button className="btn" type="submit" disabled={busy || enabled === null}>
                Maslahat olish
              </button>
            </div>
          </form>
        </>
      )}
      <p className="fine">
        Javobni sun’iy intellekt yozadi va u xato qilishi mumkin. Bu umumiy huquqiy ma’lumot, advokat maslahati emas:
        muhim qaror oldidan moddani lex.uz’da tekshiring yoki advokatga murojaat qiling. Savolga shaxsiy
        ma’lumotlarni (pasport, JShShIR, manzil) yozmang.
      </p>
    </div>
  );
}
