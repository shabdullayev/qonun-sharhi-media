import type { MetadataRoute } from "next";
import { SITE_URL, cardPath } from "@/lib/content";
import { getContent } from "@/lib/data";

export const revalidate = 1800;

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const m = await getContent();
  const now = new Date();
  return [
    { url: `${SITE_URL}/`, lastModified: now, changeFrequency: "weekly", priority: 1 },
    { url: `${SITE_URL}/yuridik-maslahat`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    ...m.sections.map((s) => ({ url: `${SITE_URL}/bolim/${s.id}`, lastModified: now, changeFrequency: "weekly" as const, priority: 0.8 })),
    ...m.cards.map((c) => ({ url: SITE_URL + cardPath(m, c), lastModified: now, changeFrequency: "monthly" as const, priority: 0.7 })),
  ];
}
