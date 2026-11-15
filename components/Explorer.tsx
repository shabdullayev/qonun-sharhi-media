"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import CardView from "@/components/CardView";
import { cardPath, shortLawName, type Card, type Content } from "@/lib/content";

const CYR: Record<string, string> = {
  а: "a", б: "b", в: "v", г: "g", д: "d", е: "e", ё: "yo", ж: "j", з: "z", и: "i", й: "y", к: "k", л: "l",
  м: "m", н: "n", о: "o", п: "p", р: "r", с: "s", т: "t", у: "u", ф: "f", х: "x", ц: "ts", ч: "ch", ш: "sh",
  ъ: "", ь: "", э: "e", ю: "yu", я: "ya", ў: "o", қ: "q", ғ: "g", ҳ: "h",
};
/** Qidiruv uchun: kichik harf, kirilldan lotinga, tutuq belgilarisiz. */
const norm = (s: string) =>
  s
    .toLowerCase()
    .replace(/[а-яёўқғҳ]/g, (ch) => CYR[ch] ?? ch)
    .replace(/[‘’ʻʼ'`]/g, "")
    .replace(/\s+/g, " ")
    .trim();

export default function Explorer({ model }: { model: Content }) {
  const { cards: CARDS, laws: LAWS, quick: QUICK, sections: SECTIONS } = model;
  const [sec, setSec] = useState("barchasi");
  const [law, setLaw] = useState<string | null>(null);
  const [query, setQuery] = useState("");

  const hay = useMemo(
    () =>
      new Map<Card, string>(
        CARDS.map((c) => [c, norm([c.q, c.a, c.t, c.m, LAWS[c.l].name, c.s.join(" "), c.k].join(" "))]),
      ),
    [CARDS, LAWS],
  );
  const words = norm(query).split(" ").filter(Boolean);
  const hit = (c: Card) => words.every((w) => hay.get(c)!.includes(w));

  const shown = SECTIONS.filter((s) => sec === "barchasi" || sec === s.id)
    .map((s) => ({
      s,
      blocks: s.laws
        .map((l) => ({ l, list: CARDS.filter((c) => c.l === l && hit(c) && (!law || law === l)) }))
        .filter((b) => b.list.length > 0),
    }))
    .filter((x) => x.blocks.length > 0);
  const total = shown.reduce((n, x) => n + x.blocks.reduce((m, b) => m + b.list.length, 0), 0);

  const pick = (id: string) => {
    setSec(id);
    setLaw(null);
  };

  return (
    <>
      <div className="gut">
        <div className="wrap searchbox">
          <form className="search" role="search" onSubmit={(e) => e.preventDefault()}>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <circle cx="9" cy="9" r="6" stroke="currentColor" strokeWidth="2" />
              <path d="M13.5 13.5 18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
            <input
              id="q"
              type="search"
              autoComplete="off"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Vaziyatni yozing: masalan, jarima yoki aliment"
              aria-label="Maslahatlardan qidirish"
            />
            {query && (
              <button type="button" onClick={() => setQuery("")}>
                Tozalash
              </button>
            )}
          </form>
          <div className="quick">
            <span>Ko‘p so‘raladi:</span>
            {QUICK.map(([t, k]) => (
              <button
                key={t}
                type="button"
                className="term"
                data-sec={k}
                onClick={() => {
                  setQuery(t);
                  pick("barchasi");
                }}
              >
                <span className="sq" />
                {t}
              </button>
            ))}
          </div>
          <Link className="cta" href="/yuridik-maslahat">
            Javob topilmadimi? Savolingizni sun’iy intellektga bering
          </Link>
        </div>
      </div>

      <div className="tabsbar gut">
        <div className="wrap tabs" role="group" aria-label="Bo‘lim bo‘yicha saralash">
          <button type="button" className="tab" aria-pressed={sec === "barchasi"} onClick={() => pick("barchasi")}>
            Hammasi <span className="n">{CARDS.length}</span>
          </button>
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              type="button"
              className="tab"
              data-sec={s.id}
              aria-pressed={sec === s.id}
              onClick={() => pick(s.id)}
            >
              <span className="sq" />
              {s.tab} <span className="n">{CARDS.filter((c) => s.laws.includes(c.l)).length}</span>
            </button>
          ))}
          <Link className="tab ai" href="/yuridik-maslahat">
            Yuridik maslahat <span className="n">AI</span>
          </Link>
          <span className="count" aria-live="polite">
            {query.trim() ? `«${query.trim()}» bo‘yicha ${total} ta maslahat` : `${total} ta maslahat`}
          </span>
        </div>
      </div>

      <div className="gut">
        <div className="wrap main">
          {shown.map(({ s, blocks }) => {
            const multi = s.laws.length > 1;
            const n = blocks.reduce((m, b) => m + b.list.length, 0);
            return (
              <section className="sec" data-sec={s.id} key={s.id}>
                <div className="sechead">
                  <span className="tag">Bo‘lim · {n} ta maslahat</span>
                  <h2>
                    <Link href={`/bolim/${s.id}`}>{s.name}</Link>
                  </h2>
                  <p>
                    {s.desc}{" "}
                    {!multi && (
                      <a href={LAWS[s.laws[0]].url} target="_blank" rel="noopener noreferrer">
                        Qonun matni
                      </a>
                    )}
                  </p>
                  {multi && (
                    <div className="lawnav">
                      {s.laws.map((l) => (
                        <button
                          key={l}
                          type="button"
                          className="term"
                          aria-pressed={law === l}
                          onClick={() => {
                            setSec(s.id);
                            setLaw(law === l ? null : l);
                          }}
                        >
                          <span className="sq" />
                          {shortLawName(model, l)}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                {blocks.map((b) => (
                  <div className="law" key={b.l}>
                    {multi && (
                      <div className="lawhead">
                        <h3>{LAWS[b.l].name}</h3>
                        <p>
                          {LAWS[b.l].desc}{" "}
                          <a href={LAWS[b.l].url} target="_blank" rel="noopener noreferrer">
                            Kodeks matni
                          </a>
                        </p>
                      </div>
                    )}
                    <div className="list">
                      {b.list.map((c) => (
                        <CardView key={c.l + c.slug} c={c} href={cardPath(model, c)} lawUrl={LAWS[c.l].url} level={multi ? 4 : 3} />
                      ))}
                    </div>
                  </div>
                ))}
              </section>
            );
          })}
          {total === 0 && (
            <div className="empty">
              <strong>Bu so‘rov bo‘yicha tayyor maslahat topilmadi</strong>
              Boshqa so‘z bilan yozib ko‘ring, masalan «jarima» yoki «aliment». Yoki savolingizni{" "}
              <Link href="/yuridik-maslahat">«Yuridik maslahat» bo‘limida</Link> sun’iy intellektga bering.
            </div>
          )}
        </div>
      </div>
    </>
  );
}
