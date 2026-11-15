export type Card = {
  /** qonun identifikatori (laws kaliti) */
  l: string;
  slug: string;
  /** modda havolasi, masalan "JK · 37-modda" */
  m: string;
  /** qisqa mavzu */
  t: string;
  /** savol */
  q: string;
  /** javob */
  a: string;
  /** qadamlar */
  s: string[];
  /** qonun matnidan iqtibos */
  k: string;
};
export type Law = { slug: string; name: string; desc: string; url: string };
export type Section = { id: string; tab: string; name: string; desc: string; laws: string[] };
export type Content = {
  checked: string;
  bhm: string;
  sections: Section[];
  laws: Record<string, Law>;
  quick: [string, string][];
  examples: string[];
  cards: Card[];
  /** Qidiruv tizimlari egalikni tasdiqlash kodlari (ixtiyoriy). */
  verify?: { google?: string; yandex?: string };
};

export const SITE_NAME = "Qonun sharhi";
export const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000").replace(/\/+$/, "");
export const TELEGRAM = "huquq_ustuvor";
export const INSTAGRAM = "qonun_sharhi_uz";

/** Kontent fayli kutilgan ko‘rinishdami (masofadan olingan faylni tekshirish uchun). */
export function isContent(x: unknown): x is Content {
  const d = x as Content;
  return Boolean(
    d &&
      typeof d.checked === "string" &&
      Array.isArray(d.sections) &&
      Array.isArray(d.cards) &&
      d.cards.length > 0 &&
      d.laws &&
      typeof d.laws === "object" &&
      d.cards.every((c) => c && c.l && c.slug && c.q && c.a && Array.isArray(c.s)),
  );
}

/** Faqat qonuni va bo‘limi ma’lum maslahatlar hamda ichida maslahati bor bo‘limlar qoladi. */
export function buildModel(data: Content): Content {
  const cards = data.cards.filter((c) => data.laws[c.l] && data.sections.some((s) => s.laws.includes(c.l)));
  const sections = data.sections
    .map((s) => ({ ...s, laws: s.laws.filter((l) => cards.some((c) => c.l === l)) }))
    .filter((s) => s.laws.length > 0);
  return { ...data, quick: data.quick || [], examples: data.examples || [], cards, sections };
}

export const cardPath = (m: Content, c: Card) => `/${m.laws[c.l].slug}/${c.slug}`;
export const sectionOfLaw = (m: Content, l: string) => m.sections.find((s) => s.laws.includes(l))!;
export const cardsOfLaw = (m: Content, l: string) => m.cards.filter((c) => c.l === l);
export const cardsOfSection = (m: Content, s: Section) => m.cards.filter((c) => s.laws.includes(c.l));
export const lawIdBySlug = (m: Content, slug: string) => Object.keys(m.laws).find((k) => m.laws[k].slug === slug);
export const shortLawName = (m: Content, l: string) => m.laws[l].name.replace(" to‘g‘risidagi kodeks", "");
