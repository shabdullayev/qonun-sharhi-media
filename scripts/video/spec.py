# -*- coding: utf-8 -*-
"""JK 169–172 uchun ssenariy: ovoz matni (tts), kartochkalar, post matni."""

SRC = "📚 Manba: O‘zR Jinoyat kodeksi, {n}-modda (lex.uz). Maʼlumot uchun, huquqiy maslahat emas."

ARTICLES = [
    {
        "n": 169, "slot": "1700", "title": "O‘g‘rilik", "tag": "ogrilik", "emoji": "🔓", "tip_emoji": "🙅",
        "hook": "O‘zganing mulkini yashirincha olish — o‘g‘rilik",
        "name_tts": "bir yuz oltmish to‘qqizinchi",
        "name_long": "o‘g‘rilik",
        "parts": [
            {
                "pill": "1-qism",
                "tts_d": "O‘g‘rilik, ya’ni o‘zganing mol-mulkini yashirin ravishda talon-toroj qilish.",
                "tts_s": "ellik bazaviy hisoblash miqdorigacha jarima, uch yuz oltmish soatgacha majburiy jamoat ishlari, ikki yilgacha axloq tuzatish ishlari, bir yildan uch yilgacha ozodlikni cheklash yoxud uch yilgacha ozodlikdan mahrum qilish.",
                "card_d": "O‘zganing mol-mulkini yashirin ravishda talon-toroj qilish",
                "card_s": ["50 BHM gacha jarima …", "1–3 yil ozodlikni cheklash", "yoki 3 yilgacha ozodlikdan mahrum qilish"],
                "cap_d": "o‘zganing mol-mulkini yashirin ravishda talon-toroj qilish",
                "cap_s": "50 BHM gacha jarima, 360 soatgacha majburiy jamoat ishlari, 2 yilgacha axloq tuzatish ishlari, 1–3 yil ozodlikni cheklash yoki 3 yilgacha ozodlikdan mahrum qilish",
            },
            {
                "pill": "2-qism",
                "tts_d": "Kissavurlik, ancha miqdorda, oldindan til biriktirgan guruh tomonidan, uy-joy, omborxona yoki boshqa xonaga g‘ayriqonuniy kirib, yoxud elektr, issiqlik, gaz yoki suv tarmog‘iga tijorat maqsadida o‘zboshimchalik bilan ulanib sodir etilsa.",
                "tts_s": "uch yuz bazaviy hisoblash miqdorigacha jarima, ikki yildan uch yilgacha axloq tuzatish ishlari, uch yildan besh yilgacha ozodlikni cheklash yoxud uch yildan besh yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Kissavurlik, ancha miqdorda, guruh bo‘lib yoki uy-joyga kirib",
                "card_s": ["300 BHM gacha jarima …", "3–5 yil ozodlikni cheklash", "yoki 3–5 yil ozodlikdan mahrum qilish"],
                "cap_d": "kissavurlik, ancha miqdorda, oldindan til biriktirgan guruh tomonidan, uy-joy, omborxona yoki boshqa xonaga g‘ayriqonuniy kirib, elektr, issiqlik, gaz yoki suv tarmog‘iga tijorat maqsadida o‘zboshimchalik bilan ulanib",
                "cap_s": "300 BHM gacha jarima, 2–3 yil axloq tuzatish ishlari, 3–5 yil ozodlikni cheklash yoki 3–5 yil ozodlikdan mahrum qilish",
            },
            {
                "pill": "3-qism",
                "tts_d": "Takroran yoki xavfli retsidivist tomonidan, axborot tizimiga ruxsatsiz kirib yoki undan foydalanib, ko‘p miqdorda, yoxud neft va gaz quvurlarida sodir etilsa.",
                "tts_s": "besh yildan sakkiz yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Takroran, ko‘p miqdorda, axborot tizimiga ruxsatsiz kirib yoki neft-gaz quvurlarida",
                "card_s": ["5–8 yil ozodlikdan mahrum qilish"],
                "cap_d": "takroran yoki xavfli retsidivist tomonidan, axborot tizimiga ruxsatsiz kirib yoki undan foydalanib, ko‘p miqdorda, neft va gaz quvurlarida",
                "cap_s": "5–8 yil ozodlikdan mahrum qilish",
            },
            {
                "pill": "4-qism",
                "tts_d": "Juda ko‘p miqdorda, o‘ta xavfli retsidivist tomonidan, yoxud uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab sodir etilsa.",
                "tts_s": "sakkiz yildan o‘n besh yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Juda ko‘p miqdorda, o‘ta xavfli retsidivist yoki uyushgan guruh tomonidan",
                "card_s": ["8–15 yil ozodlikdan mahrum qilish"],
                "cap_d": "juda ko‘p miqdorda, o‘ta xavfli retsidivist yoki uyushgan guruh tomonidan",
                "cap_s": "8–15 yil ozodlikdan mahrum qilish",
            },
        ],
        "tip": "Birovning mulkiga ko‘z olaytirmang",
        "tip_pill": "Halol yashang!",
    },
    {
        "n": 170, "slot": "1705", "title": "Aldab zarar yetkazish", "tag": "mulkiyzarar", "emoji": "🤥", "tip_emoji": "🤝",
        "hook": "Aldab yoki ishonchni suiiste’mol qilib mulkdorga zarar yetkazish — jinoyat",
        "name_tts": "bir yuz yetmishinchi",
        "name_long": "aldash yoki ishonchni suiiste’mol qilish yo‘li bilan mulkiy zarar yetkazish",
        "parts": [
            {
                "pill": "1-qism",
                "tts_d": "Aldash yoki ishonchni suiiste’mol qilish yo‘li bilan mulkdorga ancha miqdorda zarar yetkazish, basharti bu qilmishda talon-toroj qilishning alomatlari bo‘lmasa.",
                "tts_s": "yigirma besh bazaviy hisoblash miqdorigacha jarima, uch yuz soatgacha majburiy jamoat ishlari yoki ikki yilgacha axloq tuzatish ishlari.",
                "card_d": "Aldab yoki ishonchni suiiste’mol qilib mulkdorga ancha miqdorda zarar yetkazish",
                "card_s": ["25 BHM gacha jarima,", "300 soatgacha majburiy jamoat ishlari", "yoki 2 yilgacha axloq tuzatish ishlari"],
                "cap_d": "aldash yoki ishonchni suiiste’mol qilish yo‘li bilan mulkdorga ancha miqdorda zarar yetkazish, talon-toroj alomatlari bo‘lmasa",
                "cap_s": "25 BHM gacha jarima, 300 soatgacha majburiy jamoat ishlari yoki 2 yilgacha axloq tuzatish ishlari",
            },
            {
                "pill": "2-qism",
                "tts_d": "Takroran yoki xavfli retsidivist tomonidan, moddiy javobgar shaxs tomonidan, yoxud ko‘p miqdorda zarar yetkazgan holda sodir etilsa.",
                "tts_s": "yigirma beshdan ellik bazaviy hisoblash miqdorigacha jarima, uch yuz soatdan uch yuz oltmish soatgacha majburiy jamoat ishlari yoki ikki yildan uch yilgacha axloq tuzatish ishlari.",
                "card_d": "Takroran, moddiy javobgar shaxs tomonidan yoki ko‘p miqdorda zarar yetkazib",
                "card_s": ["25–50 BHM jarima,", "300–360 soat majburiy jamoat ishlari", "yoki 2–3 yil axloq tuzatish ishlari"],
                "cap_d": "takroran yoki xavfli retsidivist tomonidan, moddiy javobgar shaxs tomonidan, ko‘p miqdorda zarar yetkazib",
                "cap_s": "25–50 BHM jarima, 300–360 soat majburiy jamoat ishlari yoki 2–3 yil axloq tuzatish ishlari",
            },
        ],
        "tip": "Ishonchni oqlang, birovning haqiga xiyonat qilmang",
        "tip_pill": "Ishonchni oqlang!",
    },
    {
        "n": 171, "slot": "2100", "title": "Jinoiy mulkni olish", "tag": "jinoiymulk", "emoji": "📦", "tip_emoji": "🧾",
        "hook": "O‘g‘irlangan narsani bila turib sotib olish ham jinoyat",
        "name_tts": "bir yuz yetmish birinchi",
        "name_long": "jinoiy yo‘l bilan topilgan mulkni olish yoki o‘tkazish",
        "parts": [
            {
                "pill": "1-qism",
                "tts_d": "Mulkning jinoiy yo‘l bilan topilganini bila turib, uni oldindan va’da qilmagan holda olish yoki o‘tkazish.",
                "tts_s": "yigirma besh bazaviy hisoblash miqdorigacha jarima, uch yuz soatgacha majburiy jamoat ishlari yoki ikki yilgacha axloq tuzatish ishlari.",
                "card_d": "Jinoiy yo‘l bilan topilganini bila turib mulkni olish yoki o‘tkazish",
                "card_s": ["25 BHM gacha jarima,", "300 soatgacha majburiy jamoat ishlari", "yoki 2 yilgacha axloq tuzatish ishlari"],
                "cap_d": "mulkning jinoiy yo‘l bilan topilganini bila turib, uni oldindan va’da qilmagan holda olish yoki o‘tkazish",
                "cap_s": "25 BHM gacha jarima, 300 soatgacha majburiy jamoat ishlari yoki 2 yilgacha axloq tuzatish ishlari",
            },
            {
                "pill": "2-qism",
                "tts_d": "Takroran yoki xavfli retsidivist tomonidan, yoxud ko‘p miqdorda sodir etilsa.",
                "tts_s": "yigirma beshdan ellik bazaviy hisoblash miqdorigacha jarima, uch yuz soatdan uch yuz oltmish soatgacha majburiy jamoat ishlari, ikki yildan uch yilgacha axloq tuzatish ishlari, bir yildan uch yilgacha ozodlikni cheklash yoxud uch yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Takroran yoki ko‘p miqdorda",
                "card_s": ["25–50 BHM jarima …", "1–3 yil ozodlikni cheklash", "yoki 3 yilgacha ozodlikdan mahrum qilish"],
                "cap_d": "takroran yoki xavfli retsidivist tomonidan, ko‘p miqdorda",
                "cap_s": "25–50 BHM jarima, 300–360 soat majburiy jamoat ishlari, 2–3 yil axloq tuzatish ishlari, 1–3 yil ozodlikni cheklash yoki 3 yilgacha ozodlikdan mahrum qilish",
            },
            {
                "pill": "3-qism",
                "tts_d": "Juda ko‘p miqdorda, o‘ta xavfli retsidivist tomonidan, yoxud uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab sodir etilsa.",
                "tts_s": "ellikdan yuz bazaviy hisoblash miqdorigacha jarima, uch yildan besh yilgacha ozodlikni cheklash yoxud uch yildan besh yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Juda ko‘p miqdorda, o‘ta xavfli retsidivist yoki uyushgan guruh tomonidan",
                "card_s": ["50–100 BHM jarima,", "3–5 yil ozodlikni cheklash", "yoki 3–5 yil ozodlikdan mahrum qilish"],
                "cap_d": "juda ko‘p miqdorda, o‘ta xavfli retsidivist tomonidan, uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab",
                "cap_s": "50–100 BHM jarima, 3–5 yil ozodlikni cheklash yoki 3–5 yil ozodlikdan mahrum qilish",
            },
        ],
        "tip": "Kelib chiqishi shubhali narsani sotib olmang",
        "tip_pill": "Shubhali molni olmang!",
    },
    {
        "n": 172, "slot": "2105", "title": "Mulkni vijdonsiz qo‘riqlash", "tag": "mulkniqoriqlash", "emoji": "🔐", "tip_emoji": "🛡️",
        "hook": "Qo‘riqlashga topshirilgan mulkka beparvo qarash ham jinoyat bo‘lishi mumkin",
        "name_tts": "bir yuz yetmish ikkinchi",
        "name_long": "mulkni qo‘riqlashga vijdonsiz munosabatda bo‘lish",
        "parts": [
            {
                "pill": "Modda mazmuni",
                "tts_d": "Shaxsning mulkni qo‘riqlash yuzasidan o‘z vazifalarini vijdonsiz bajarishi natijasida mol-mulk talon-toroj qilinishi, unga shikast yetkazilishi yoki uning nobud qilinishi ko‘p miqdorda zarar yetkazilishiga sabab bo‘lsa, basharti bu qilmishda mansabdorlik jinoyati alomatlari bo‘lmasa.",
                "tts_s": "ellik bazaviy hisoblash miqdorigacha jarima, uch yuz soatgacha majburiy jamoat ishlari yoki ikki yilgacha axloq tuzatish ishlari.",
                "card_d": "Qo‘riqlash vazifasini vijdonsiz bajarish oqibatida mulkka ko‘p miqdorda zarar yetishi",
                "card_s": ["50 BHM gacha jarima,", "300 soatgacha majburiy jamoat ishlari", "yoki 2 yilgacha axloq tuzatish ishlari"],
                "cap_d": "mulkni qo‘riqlash vazifasini vijdonsiz bajarish natijasida mol-mulk talon-toroj qilinishi, shikastlanishi yoki nobud bo‘lishi ko‘p miqdorda zarar yetkazsa, mansabdorlik jinoyati alomatlari bo‘lmasa",
                "cap_s": "50 BHM gacha jarima, 300 soatgacha majburiy jamoat ishlari yoki 2 yilgacha axloq tuzatish ishlari",
                "cap_label": "Modda",
            },
        ],
        "tip": "Sizga ishonib topshirilgan mulkni ko‘z qorachig‘idek asrang",
        "tip_pill": "Omonatni asrang!",
    },
]

ORD = ["Birinchi", "Ikkinchi", "Uchinchi", "To‘rtinchi"]


def tts_apos(s):
    return s.replace("‘", "ʻ").replace("’", "ʼ")


def segments(a):
    """Har bir segment: (ovoz matni, kartochka pill, kartochka asosiy matn, yashil qatorlar)."""
    cap = lambda s: s[0].upper() + s[1:]
    segs = [
        (a["hook"] + ".", a["title"], a["hook"], []),
        (f"Jinoyat kodeksining {a['name_tts']} moddasi. {cap(a['name_long'])}.", f"JK {a['n']}-modda", cap(a["name_long"]), []),
    ]
    single = len(a["parts"]) == 1
    for i, p in enumerate(a["parts"]):
        lead = "" if single else ORD[i] + " qism. "
        segs.append((lead + p["tts_d"] + " Jazo: " + p["tts_s"], p["pill"], p["card_d"], p["card_s"]))
    segs.append((a["tip"] + ". Qonun sharhi. Do‘stlaringizga ulashing.", a["tip_pill"], "Qonun sharhi · Do‘stlaringizga ulashing", []))
    return segs


def caption(a, hashtags=True):
    lines = [f"{a['hook']} {a['emoji']}", "", f"JK {a['n']}-modda qisqacha ({a['name_long']}):"]
    for p in a["parts"]:
        lines.append(f"▫️ {p.get('cap_label', p['pill'])} ({p['cap_d']}): {p['cap_s']}")
    lines += ["", f"{a['tip']} {a['tip_emoji']}", "", SRC.format(n=a["n"])]
    if hashtags:
        lines += ["", f"#qonunsharhi #jinoyatkodeksi #{a['n']}modda #{a['tag']} #huquq"]
    return "\n".join(lines)


if __name__ == "__main__":
    import json, os, sys
    out = sys.argv[1]
    for a in ARTICLES:
        d = {"voice": "uz-UZ-MadinaNeural", "segments": [tts_apos(s[0]) for s in segments(a)]}
        json.dump(d, open(os.path.join(out, f"jk{a['n']}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(caption(a), "\n")
