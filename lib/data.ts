import bundled from "@/data/content.json";
import { buildModel, isContent, type Content } from "@/lib/content";

/**
 * Kontent manbai. Sayt har 30 daqiqada shu manzildagi faylni qayta o‘qiydi, shuning uchun
 * yangi maslahat qo‘shish uchun saytni qayta joylash shart emas: faylni yangilash kifoya.
 * CONTENT_URL bo‘sh satr qilib berilsa, faqat loyiha ichidagi data/content.json ishlatiladi.
 */
const CONTENT_URL =
  process.env.CONTENT_URL ??
  "https://raw.githubusercontent.com/shabdullayev/qonun-sharhi-media/sayt/data/content.json";

export async function getContent(): Promise<Content> {
  if (CONTENT_URL) {
    try {
      const res = await fetch(CONTENT_URL, { next: { revalidate: 1800 } });
      if (res.ok) {
        const data: unknown = await res.json();
        if (isContent(data)) return buildModel(data);
      }
    } catch {
      // tarmoq xatosi: loyiha ichidagi nusxaga qaytamiz
    }
  }
  return buildModel(bundled as unknown as Content);
}
