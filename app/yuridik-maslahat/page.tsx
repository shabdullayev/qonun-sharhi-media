import type { Metadata } from "next";
import Link from "next/link";
import Advice from "@/components/Advice";
import { getContent } from "@/lib/data";

export const revalidate = 1800;

export const metadata: Metadata = {
  title: "Yuridik maslahat: sun’iy intellekt savolingizga javob beradi",
  description:
    "Savolingizni oddiy so‘zlar bilan yozing: sun’iy intellekt O‘zbekiston qonunchiligi va saytdagi tekshirilgan maslahatlar asosida avtomatik javob beradi.",
  alternates: { canonical: "/yuridik-maslahat" },
};

export default async function AdvicePage() {
  const { examples } = await getContent();
  return (
    <div className="gut" data-sec="maslahat">
      <div className="wrap">
        <nav className="crumbs" aria-label="Yo‘l">
          <Link href="/">Bosh sahifa</Link>
          <span>/</span>
          <span>Yuridik maslahat</span>
        </nav>
        <section className="advice">
          <div className="sechead">
            <span className="tag">Sun’iy intellekt · avtomatik javob</span>
            <h1>Yuridik maslahat</h1>
            <p>
              Savolingizni oddiy so‘zlar bilan yozing. Javob O‘zbekiston qonunchiligi va shu saytdagi tekshirilgan
              maslahatlar asosida avtomatik tayyorlanadi.
            </p>
          </div>
          <div className="desk">
            <div className="side">
              <b>Qanday ishlaydi</b>
              <span>
                Savol yuborasiz, sun’iy intellekt bir daqiqa ichida javob yozadi: qisqa xulosa, qadamlar va tayanilgan
                qonun.
              </span>
              <span>Davom ettirib, aniqlashtiruvchi savol berishingiz mumkin.</span>
            </div>
            <Advice examples={examples} />
          </div>
        </section>
      </div>
    </div>
  );
}
