# qonun-sharhi-media

Qonun sharhi Instagram kanali uchun video fayllar (Buffer orqali joylash uchun ochiq havolalar).

## Tuzilishi

- `videos/YYYY-MM-DD/HHMM_nom.mp4` — har bir post uchun video (vaqt — Toshkent vaqti).
- `queue/queue.json` — post navbati: sana, vaqt, matn va videoning commit'ga bog‘langan havolasi.

Har kuni kechqurun avtomatik vazifa `queue/queue.json` dan ertangi kun postlarini o‘qib, Buffer'ga
(Instagram: @qonun_sharhi_uz) rejalashtiradi. Navbatda bo‘lmagan post joylanmaydi.
