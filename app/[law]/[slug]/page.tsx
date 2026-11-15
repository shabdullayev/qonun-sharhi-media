import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SITE_URL, cardPath, cardsOfLaw, lawIdBySlug, sectionOfLaw, type Content } from "@/lib/content";
import { getContent } from "@/lib/data";

export const revalidate = 1800;
export const dynamicParams = true;
export const generateStaticParams = async () => {
  const m = await getContent();
  return m.cards.map((c) => ({ law: m.laws[c.l].slug, slug: c.slug }));
};

type Props = { params: Promise<{ law: string; slug: string }> };

function find(m: Content, law: string, slug: string) {
  const id = lawIdBySlug(m, law);
  return id ? m.cards.find((c) => c.l === id && c.slug === slug) : undefined;
}

const clip = (s: string, n = 158) => (s.length <= n ? s : s.slice(0, s.lastIndexOf(" ", n)) + "…");

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { law, slug } = await params;
  const m = await getContent();
  const c = find(m, law, slug);
  if (!c) return {};
  return {
    title: c.q,
    description: clip(c.a),
    alternates: { canonical: cardPath(m, c) },
    openGraph: { type: "article", title: c.q, description: clip(c.a), url: cardPath(m, c) },
  };
}

export default async function CardPage({ params }: Props) {
  const { law, slug } = await params;
  const m = await getContent();
  const c = find(m, law, slug);
  if (!c) notFound();
  const L = m.laws[c.l];
  const s = sectionOfLaw(m, c.l);
  const others = cardsOfLaw(m, c.l).filter((x) => x !== c);
  const jsonLd = [
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      inLanguage: "uz",
      mainEntity: [
        {
          "@type": "Question",
          name: c.q,
          acceptedAnswer: { "@type": "Answer", text: `${c.a} Nima qilish kerak: ${c.s.join(" ")} (${c.m})` },
        },
      ],
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Bosh sahifa", item: SITE_URL + "/" },
        { "@type": "ListItem", position: 2, name: s.name, item: `${SITE_URL}/bolim/${s.id}` },
        { "@type": "ListItem", position: 3, name: c.t, item: SITE_URL + cardPath(m, c) },
      ],
    },
  ];
  return (
    <div data-sec={s.id}>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c") }} />
      <div className="gut">
        <div className="wrap">
          <nav className="crumbs" aria-label="Yo‘l">
            <Link href="/">Bosh sahifa</Link>
            <span>/</span>
            <Link href={`/bolim/${s.id}`}>{s.name}</Link>
            <span>/</span>
            <span>{L.name}</span>
          </nav>
          <article className="page">
            <div className="cite">
              <span className="ref">
                <span className="sq" />
                {c.m}
              </span>
              <span className="topic">{c.t}</span>
              <span className="topic">Tekshirilgan: {m.checked}</span>
            </div>
            <div className="body">
              <h1>{c.q}</h1>
              <p className="lede">{c.a}</p>
              <h2>Nima qilish kerak</h2>
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
                  <a href={L.url} target="_blank" rel="noopener noreferrer">
                    lex.uz’da to‘liq o‘qish
                  </a>
                </span>
              </div>
              <p className="fine">
                Bu umumiy huquqiy ma’lumot, advokat maslahati emas. Aniq ish bo‘yicha advokatga yoki tegishli davlat
                organiga murojaat qiling.
              </p>
              <Link className="cta" href="/yuridik-maslahat">
                Vaziyatingiz boshqacharoqmi? Savolingizni sun’iy intellektga bering
              </Link>
            </div>
          </article>
          {others.length > 0 && (
            <section className="others">
              <h2>{L.name}: boshqa maslahatlar</h2>
              <ul>
                {others.map((x) => (
                  <li key={x.slug}>
                    <span>{x.m}</span>
                    <Link href={cardPath(m, x)}>{x.q}</Link>
                  </li>
                ))}
              </ul>
            </section>
          )}
        </div>
      </div>
    </div>
  );
}
