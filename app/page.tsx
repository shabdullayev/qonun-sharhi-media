import type { Metadata } from "next";
import Explorer from "@/components/Explorer";
import { SITE_NAME, SITE_URL } from "@/lib/content";
import { getContent } from "@/lib/data";

export const revalidate = 1800;

export const metadata: Metadata = { alternates: { canonical: "/" } };

export default async function Home() {
  const model = await getContent();
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: SITE_NAME,
    url: SITE_URL,
    inLanguage: "uz",
    description: "O‘zbekiston qonunlari bo‘yicha hayotiy maslahatlar.",
  };
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c") }} />
      <div className="gut">
        <section className="wrap hero">
          <div className="eyebrow">Qonunlar bo‘yicha hayotiy maslahatlar</div>
          <h1>
            Qonun nima deydi? <em>Oddiy tilda.</em>
          </h1>
          <p className="lead">
            Kodekslar, Konstitutsiya va huquq-tartibot qonunlaridagi qoidalar kundalik vaziyatlar ko‘rinishida. Har bir
            javob yonida modda raqami, qonun matnidan iqtibos va lex.uz havolasi bor.
          </p>
        </section>
      </div>
      <Explorer model={model} />
    </>
  );
}
