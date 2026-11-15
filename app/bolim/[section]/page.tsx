import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CardView from "@/components/CardView";
import { cardPath, cardsOfLaw, cardsOfSection } from "@/lib/content";
import { getContent } from "@/lib/data";

export const revalidate = 1800;
export const dynamicParams = true;
export const generateStaticParams = async () => (await getContent()).sections.map((s) => ({ section: s.id }));

type Props = { params: Promise<{ section: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { section } = await params;
  const m = await getContent();
  const s = m.sections.find((x) => x.id === section);
  if (!s) return {};
  return {
    title: `${s.name} bo‘yicha hayotiy maslahatlar`,
    description: `${s.desc} ${cardsOfSection(m, s).length} ta savol-javob, har birida modda raqami va lex.uz havolasi.`,
    alternates: { canonical: `/bolim/${s.id}` },
  };
}

export default async function SectionPage({ params }: Props) {
  const { section } = await params;
  const m = await getContent();
  const LAWS = m.laws;
  const s = m.sections.find((x) => x.id === section);
  if (!s) notFound();
  const multi = s.laws.length > 1;
  return (
    <div className="gut" data-sec={s.id}>
      <div className="wrap">
        <nav className="crumbs" aria-label="Yo‘l">
          <Link href="/">Bosh sahifa</Link>
          <span>/</span>
          <span>{s.name}</span>
        </nav>
        <div className="main">
          <section className="sec">
            <div className="sechead">
              <span className="tag">Bo‘lim · {cardsOfSection(m, s).length} ta maslahat</span>
              <h1>{s.name}</h1>
              <p>
                {s.desc}{" "}
                {!multi && (
                  <a href={LAWS[s.laws[0]].url} target="_blank" rel="noopener noreferrer">
                    Qonun matni
                  </a>
                )}
              </p>
            </div>
            {s.laws.map((l) => (
              <div className="law" key={l}>
                {multi && (
                  <div className="lawhead">
                    <h2>{LAWS[l].name}</h2>
                    <p>
                      {LAWS[l].desc}{" "}
                      <a href={LAWS[l].url} target="_blank" rel="noopener noreferrer">
                        Rasmiy matn
                      </a>
                    </p>
                  </div>
                )}
                <div className="list">
                  {cardsOfLaw(m, l).map((c) => (
                    <CardView key={c.slug} c={c} href={cardPath(m, c)} lawUrl={LAWS[l].url} level={3} />
                  ))}
                </div>
              </div>
            ))}
          </section>
        </div>
      </div>
    </div>
  );
}
