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

## Video sifati (2026-11-20 dan, yangi videolar uchun)

Kelgusi videolarda animatsiya va grafika yuqori sifatda bo‘lishi kerak. JK 162 gacha tayyorlangan
videolar o‘zgarishsiz qoladi.

- O‘lcham 1080×1920 (9:16), kadr chastotasi 30 fps; sahnalar va qahramonlar kamida 1080×1920
  o‘lchamda chiziladi (kichik rasmni kattalashtirish yo‘q), matn va grafika aniq, qirralari silliq.
- Animatsiya silliq: keskin sakrashsiz harakat, sahnalar orasida o‘tish effektlari, kamera harakati
  (zoom/pan) yumshoq.
- Kodlash: H.264 High, `-crf 18 -preset slow`, `-maxrate 10M -bufsize 20M`, `-pix_fmt yuv420p`,
  rang `bt709` (`-colorspace bt709 -color_primaries bt709 -color_trc bt709`), `-movflags +faststart`;
  ovoz AAC 48 kHz, 192 kbit/s. Avvalgi videolar ~0,35 Mbit/s bitreyt bilan chiqqan edi — bu grafikani
  xira va «kvadrat» qilib yuboradi; yangi videolarda video bitreyti taxminan 6–10 Mbit/s bo‘lsin.
- Birinchi kadr qora bo‘lmasin (muqova uchun): video darhol rangli sahnadan boshlansin.

## Vizual uslub (2026-11-20 dan, yangi videolar uchun)

Asadbek ko‘rsatgan namuna asosida: hozirgi oddiy geometrik shakllar va to‘q ko‘k fon o‘rniga
**qo‘lda chizilgandek, iliq, «podkast/hikoya» uslubidagi illyustratsiya**.

- Fon: och krem / iliq rangli, mayda detallar (stol, kitoblar, gul, krujka, mikrofon kabi) bilan
  qulay muhit; sahnaga mos joy (sud zali, uy, ko‘cha, idora) ham shu uslubda.
- Qahramonlar: aniq kontur chiziqli, yumshoq soyali, yuz ifodalari jonli (gapirish, hayrat,
  tashvish, tabassum), qo‘l harakatlari bilan; doimiy 2 ta boshlovchi (yigit va qiz) hamda
  syujetga qarab qo‘shimcha obrazlar. Qahramonlar barcha videolarda bir xil ko‘rinishda qoladi.
- Sarlavha: katta, qalin, konturli harflar (to‘q qizil va to‘q yashil kabi kontrast ranglar),
  qisqa va yirik — masalan «JK 157 · Davlatga xoinlik».
- Animatsiya: gapirayotganda og‘iz va qo‘l harakati, ko‘z pirpiratish, yengil kamera zoom/pan,
  matn kartochkalari yumshoq paydo bo‘ladi; yuqoridagi «Video sifati» talablari ham amal qiladi.
- Namunadagi personajlar, yozuvlar yoki brendlar aynan ko‘chirilmaydi — faqat uslub olinadi.
