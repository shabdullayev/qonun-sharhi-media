# Qonun sharhi

Qonunlar bo‘yicha hayotiy maslahatlar sayti: Next.js (App Router), barcha sahifalar statik HTML sifatida yig‘iladi, shuning uchun qidiruv tizimlari ularni to‘liq o‘qiydi.

## Tuzilishi

| Manzil | Nima |
|---|---|
| `/` | Bosh sahifa: qidiruv, bo‘limlar, barcha maslahatlar |
| `/bolim/<bo‘lim>` | Bitta bo‘lim (masalan, `/bolim/kodekslar`) |
| `/<qonun>/<maslahat>` | Har bir maslahatning o‘z sahifasi (masalan, `/oila-kodeksi/aliment-miqdori`) |
| `/yuridik-maslahat` | Sun’iy intellekt bilan savol-javob |
| `/sitemap.xml`, `/robots.txt` | Qidiruv tizimlari uchun, avtomatik yig‘iladi |
| `/api/maslahat` | AI javobini beradigan server yo‘li |

Butun kontent bitta faylda: `data/content.json`. Yangi maslahat qo‘shish uchun `cards` ro‘yxatiga yozuv qo‘shiladi, sahifa, sitemap va AI ko‘rsatmasi o‘zi yangilanadi.

## Ishga tushirish

```bash
npm install
cp .env.example .env.local   # qiymatlarni to‘ldiring
npm run dev                  # http://localhost:3000
```

Node.js 20 yoki undan yangi versiya kerak.

## Sozlamalar (`.env.local` yoki hosting paneli)

| O‘zgaruvchi | Vazifasi |
|---|---|
| `NEXT_PUBLIC_SITE_URL` | Saytning to‘liq manzili, masalan `https://qonunsharhi.uz`. Sitemap, canonical va Open Graph shundan olinadi. Vercel’da bo‘sh qoldirilsa, loyihaning asosiy domeni olinadi. |
| `ANTHROPIC_API_KEY` | AI maslahat uchun Claude API kaliti. Bo‘sh bo‘lsa, «Yuridik maslahat» sahifasi formani ko‘rsatmaydi. |
| `ANTHROPIC_MODEL` | Ixtiyoriy. Standart: `claude-sonnet-5-5`; arzonroq: `claude-haiku-5-5`. |
| `CONTENT_URL` | Ixtiyoriy. Kontent fayli olinadigan manzil. Sayt uni har 30 daqiqada qayta o‘qiydi, shuning uchun yangi maslahat qo‘shish uchun qayta joylash shart emas. Bo‘sh satr berilsa, faqat `data/content.json` ishlatiladi. |

AI har bir savol uchun pullik so‘rov yuboradi. Xarajatni cheklash uchun bitta IP manzildan 10 daqiqada 6 ta savol qabul qilinadi (`app/api/maslahat/route.ts` ichidagi `LIMIT`).

## Joylash

### Vercel
1. Loyihani GitHub omboriga yuklang.
2. vercel.com’da omborni import qiling.
3. Yuqoridagi uchta o‘zgaruvchini kiriting va domenni ulang.

### O‘z serveringiz (VPS)
```bash
npm ci && npm run build
cp -r .next/static .next/standalone/.next/static
PORT=3000 node .next/standalone/server.js
```
Oldiga nginx qo‘yib, domen va HTTPS sertifikatini ulang. Jarayonni pm2 yoki systemd orqali doimiy ishlatib turing.

## Qidiruv tizimlariga chiqarish

1. Sayt domenda ochilgach, Google Search Console va Yandex Webmaster’da domenni tasdiqlang.
2. Ikkalasiga ham `https://<domen>/sitemap.xml` manzilini yuboring.
3. Indekslash odatda bir necha kundan bir necha haftagacha vaqt oladi.

## Eslatma

Maslahatlar `data/content.json` ichidagi `checked` sanasi holatiga lex.uz bilan solishtirilgan. Qonun o‘zgarsa, tegishli yozuvni va sanani yangilang.
