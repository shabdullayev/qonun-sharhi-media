# qonun-sharhi-media

Qonun sharhi Instagram kanali uchun video fayllar (Buffer orqali joylash uchun ochiq havolalar).

## Tuzilishi

- `videos/YYYY-MM-DD/HHMM_nom.mp4` — har bir post uchun video (vaqt — Toshkent vaqti).
- `queue/queue.json` — post navbati: sana, vaqt, matn va videoning commit'ga bog‘langan havolasi.

## Qoida

Faqat yangi moddalar ketma-ket joylanadi (JK 110, 111, 112 …). Avval joylangan moddalardan
qirqilgan klip yoki takror videolar navbatga qo‘yilmaydi. `videos/2026-11-10 … 2026-11-13` dagi
eski kliplar bekor qilingan va navbatda yo‘q.

Har kuni 22:30 da avtomatik vazifa `queue/queue.json` dan ertangi kun postlarini o‘qib, Buffer'ga
(Instagram: @qonun_sharhi_uz) rejalashtiradi. Navbatda bo‘lmagan post joylanmaydi.

## Ovoz

Ovoz `scripts/tts.py` orqali (edge-tts, `uz-UZ-MadinaNeural`) yaratiladi. 2026-11-16 dan boshlab
yangi videolarda ovoz tempi biroz tezroq: standart `rate` = `+15%`. Kerak bo‘lsa
`tts/in/<kalit>.json` ga `"rate": "+20%"` kabi qiymat qo‘shib o‘zgartiriladi. JK 148 gacha
tayyorlangan videolar o‘zgarishsiz qoladi.
