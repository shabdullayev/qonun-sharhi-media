import Link from "next/link";
import type { Card } from "@/lib/content";

/** Ro‘yxatdagi bitta maslahat: chapda modda, o‘ngda savol va javob. */
export default function CardView({ c, href, lawUrl, level = 3 }: { c: Card; href: string; lawUrl: string; level?: 3 | 4 }) {
  const H = level === 3 ? "h3" : "h4";
  return (
    <article className="card">
      <div className="cite">
        <span className="ref">
          <span className="sq" />
          {c.m}
        </span>
        <span className="topic">{c.t}</span>
      </div>
      <div className="body">
        <H className="qh">
          <Link href={href}>{c.q}</Link>
        </H>
        <p className="ans">{c.a}</p>
        <details>
          <summary>Nima qilish kerak va qonunda qanday yozilgan</summary>
          <ol className="steps">
            {c.s.map((x, i) => (
              <li key={i}>
                <span>{x}</span>
              </li>
            ))}
          </ol>
          <div className="lawq">
            <span className="lbl">Qonun matnidan</span>
            <q>{c.k}</q>
            <span className="src">
              {c.m} ·{" "}
              <a href={lawUrl} target="_blank" rel="noopener noreferrer">
                lex.uz’da to‘liq o‘qish
              </a>
            </span>
          </div>
        </details>
      </div>
    </article>
  );
}
