import type { Metadata, Viewport } from "next";
import Link from "next/link";
import "./globals.css";
import { INSTAGRAM, SITE_NAME, SITE_URL, TELEGRAM } from "@/lib/content";
import { getContent } from "@/lib/data";

const DESCRIPTION =
  "O‘zbekiston qonunlari bo‘yicha hayotiy maslahatlar: jarima, aliment, ajrashish, haqorat va boshqa vaziyatlarda qonun nima deyishi sodda tilda, modda raqami va lex.uz havolasi bilan.";

export async function generateMetadata(): Promise<Metadata> {
  const { verify } = await getContent();
  return { ...BASE, verification: verify ? { google: verify.google, yandex: verify.yandex } : undefined };
}

const BASE: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: "Qonun sharhi — qonunlar bo‘yicha hayotiy maslahatlar", template: "%s · Qonun sharhi" },
  description: DESCRIPTION,
  applicationName: SITE_NAME,
  openGraph: { type: "website", siteName: SITE_NAME, locale: "uz_UZ", description: DESCRIPTION },
  robots: { index: true, follow: true },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f1f3f7" },
    { media: "(prefers-color-scheme: dark)", color: "#0e131d" },
  ],
};

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const { sections: SECTIONS, checked: CHECKED, bhm: BHM } = await getContent();
  return (
    <html lang="uz">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Zilla+Slab:ital,wght@0,500;0,700;1,500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap"
        />
      </head>
      <body>
        <div className="gut">
          <header className="wrap top">
            <Link className="brand" href="/">
              <svg width="30" height="30" viewBox="0 0 30 30" aria-hidden="true">
                <rect width="30" height="30" rx="7" fill="var(--ink)" />
                <path d="M12 9.2v11.6L21 15z" fill="var(--paper)" />
              </svg>
              {SITE_NAME}
            </Link>
            <nav aria-label="Asosiy bo‘limlar">
              {SECTIONS.map((s) => (
                <Link key={s.id} href={`/bolim/${s.id}`}>
                  {s.tab}
                </Link>
              ))}
              <Link href="/yuridik-maslahat">Yuridik maslahat</Link>
            </nav>
          </header>
        </div>

        {children}

        <footer className="about gut">
          <div className="wrap">
            <h2>Loyiha haqida</h2>
            <div>
              <div className="links">
                <Link href="/">Bosh sahifa</Link>
                {SECTIONS.map((s) => (
                  <Link key={s.id} href={`/bolim/${s.id}`}>
                    {s.name}
                  </Link>
                ))}
                <Link href="/yuridik-maslahat">Yuridik maslahat</Link>
                <a href={`https://t.me/${TELEGRAM}`} target="_blank" rel="noopener noreferrer">
                  Telegram: @{TELEGRAM}
                </a>
                <a href={`https://www.instagram.com/${INSTAGRAM}/`} target="_blank" rel="noopener noreferrer">
                  Instagram: @{INSTAGRAM}
                </a>
              </div>
              <p>
                «Qonun sharhi» qonunlarni oddiy tilda tushuntiradi: Instagram’da Jinoyat kodeksi moddalari bo‘yicha qisqa
                videolar, Telegram’da <span className="handle">@{TELEGRAM}</span> kanali, bu saytda esa qonunlar bo‘yicha
                hayotiy maslahatlar.
              </p>
              <p>
                Har bir maslahat qonunning lex.uz’dagi amaldagi matni bilan {CHECKED} holatiga solishtirilgan. Jarimalar
                BHM (bazaviy hisoblash miqdori) baravarida ko‘rsatilgan; BHM {BHM}. Qonunlar o‘zgarib turadi, shuning
                uchun muhim qaror oldidan moddani havola orqali o‘zingiz ham o‘qib chiqing.
              </p>
              <p className="fine">
                Sayt umumiy huquqiy ma’lumot beradi va advokat maslahatining o‘rnini bosmaydi. Aniq ish bo‘yicha
                advokatga yoki tegishli davlat organiga murojaat qiling.
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
