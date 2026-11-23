# -*- coding: utf-8 -*-
"""JK 173, 175–179 uchun ssenariy (174-modda kuchini yo‘qotgan): ovoz matni (tts), kartochkalar, post matni."""

SRC = "📚 Manba: O‘zR Jinoyat kodeksi, {n}-modda (lex.uz). Maʼlumot uchun, huquqiy maslahat emas."

ARTICLES = [
    {
        "n": 173, "slot": "1300", "title": "Mulkni qasddan buzish", "tag": "mulkninobudqilish", "emoji": "🔨", "tip_emoji": "🤲",
        "hook": "O‘zganing mulkini ataylab buzish yoki nobud qilish — jinoyat",
        "name_tts": "bir yuz yetmish uchinchi",
        "name_long": "mulkni qasddan nobud qilish yoki unga zarar yetkazish",
        "parts": [
            {
                "pill": "1-qism",
                "tts_d": "O‘zganing mol-mulkini qasddan nobud qilish yoki unga zarar yetkazish, agar zarar ancha miqdorni tashkil etsa.",
                "tts_s": "ellik baravaridan yetmish besh baravarigacha bazaviy hisoblash miqdorida jarima, uch yuz soatgacha majburiy jamoat ishlari yoki ikki yilgacha axloq tuzatish ishlari.",
                "card_d": "O‘zganing mulkini qasddan nobud qilish yoki shikastlash (ancha miqdorda zarar)",
                "card_s": ["50–75 BHM jarima,", "300 soatgacha majburiy jamoat ishlari", "yoki 2 yilgacha axloq tuzatish ishlari"],
                "cap_d": "o‘zganing mol-mulkini qasddan nobud qilish yoki unga zarar yetkazish, zarar ancha miqdorda bo‘lsa",
                "cap_s": "50–75 BHM jarima, 300 soatgacha majburiy jamoat ishlari yoki 2 yilgacha axloq tuzatish ishlari",
            },
            {
                "pill": "2-qism",
                "tts_d": "Millatlararo, irqiy yoki diniy adovat zamirida, atrofdagilar uchun xavfli usulda, yoxud ko‘p miqdorda zarar yetkazgan holda sodir etilsa.",
                "tts_s": "yetmish besh baravaridan yuz baravarigacha bazaviy hisoblash miqdorida jarima, uch yuz soatdan uch yuz oltmish soatgacha majburiy jamoat ishlari, ikki yildan uch yilgacha axloq tuzatish ishlari, bir yildan uch yilgacha ozodlikni cheklash yoxud uch yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Adovat zamirida, xavfli usulda yoki ko‘p miqdorda zarar yetkazib",
                "card_s": ["75–100 BHM jarima …", "1–3 yil ozodlikni cheklash", "yoki 3 yilgacha ozodlikdan mahrum qilish"],
                "cap_d": "millatlararo, irqiy yoki diniy adovat zamirida, atrofdagilar uchun xavfli usulda yoki ko‘p miqdorda zarar yetkazib",
                "cap_s": "75–100 BHM jarima, 300–360 soat majburiy jamoat ishlari, 2–3 yil axloq tuzatish ishlari, 1–3 yil ozodlikni cheklash yoki 3 yilgacha ozodlikdan mahrum qilish",
            },
            {
                "pill": "3-qism",
                "tts_d": "Jabrlanuvchi yoki uning yaqin qarindoshlarining xizmat yoki fuqarolik burchini bajarishi munosabati bilan, yoxud uyushgan guruh tomonidan sodir etilsa.",
                "tts_s": "uch yildan besh yilgacha ozodlikni cheklash yoki uch yildan besh yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Xizmat yoki fuqarolik burchi uchun qasos olib yoki uyushgan guruh tomonidan",
                "card_s": ["3–5 yil ozodlikni cheklash", "yoki 3–5 yil ozodlikdan mahrum qilish"],
                "cap_d": "jabrlanuvchi yoki uning yaqinlarining xizmat yoki fuqarolik burchini bajarishi munosabati bilan, uyushgan guruh tomonidan",
                "cap_s": "3–5 yil ozodlikni cheklash yoki 3–5 yil ozodlikdan mahrum qilish",
            },
        ],
        "tip": "Birovning mulkiga zarar yetkazmang, uni asrang",
        "tip_pill": "Mulkni asrang!",
    },
    {
        "n": 175, "slot": "1305", "title": "Davlatga zararli bitim", "tag": "zararlibitim", "emoji": "📉", "tip_emoji": "🤝",
        "hook": "Davlat manfaatlariga zid bitim tuzish — og‘ir jinoyat",
        "name_tts": "bir yuz yetmish beshinchi",
        "name_long": "O‘zbekiston Respublikasining manfaatlariga xilof ravishda bitimlar tuzish",
        "parts": [
            {
                "pill": "1-qism",
                "tts_d": "Aniq foydasiz bitim tuzish, jumladan ishlatilgan, eskirgan yoki yaroqsiz uskuna va texnologiyalarni olib kirish, agar bu respublika manfaatlariga ko‘p miqdorda zarar yetkazgan bo‘lsa. Bunday bitimga imkon bergan xulosa yoki hujjatni bergan mansabdor shaxs ham javob beradi.",
                "tts_s": "uch yuz baravaridan besh yuz baravarigacha bazaviy hisoblash miqdorida jarima yoxud muayyan huquqdan mahrum qilib, uch yildan besh yilgacha ozodlikni cheklash yoki uch yildan besh yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Foydasiz bitim, eskirgan yoki yaroqsiz uskuna olib kirish — davlatga ko‘p miqdorda zarar",
                "card_s": ["300–500 BHM jarima", "yoki 3–5 yil ozodlikni cheklash", "yoki 3–5 yil ozodlikdan mahrum qilish"],
                "cap_d": "foydasiz bitim tuzish, jumladan ishlatilgan, eskirgan yoki yaroqsiz uskuna va texnologiyalarni olib kirish respublika manfaatlariga ko‘p miqdorda zarar yetkazsa; bunga imkon bergan xulosa yoki hujjatni bergan mansabdor ham javob beradi",
                "cap_s": "300–500 BHM jarima yoki muayyan huquqdan mahrum qilib 3–5 yil ozodlikni cheklash yoki 3–5 yil ozodlikdan mahrum qilish",
            },
            {
                "pill": "2-qism",
                "tts_d": "Takroran, yoxud bir guruh shaxslar tomonidan oldindan til biriktirib sodir etilsa.",
                "tts_s": "besh yildan sakkiz yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Takroran yoki oldindan til biriktirgan guruh tomonidan",
                "card_s": ["5–8 yil ozodlikdan mahrum qilish"],
                "cap_d": "takroran yoki bir guruh shaxslar tomonidan oldindan til biriktirib",
                "cap_s": "5–8 yil ozodlikdan mahrum qilish",
            },
            {
                "pill": "3-qism",
                "tts_d": "Juda ko‘p miqdorda zarar yetkazgan holda, yoxud uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab sodir etilsa.",
                "tts_s": "sakkiz yildan o‘n ikki yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Juda ko‘p miqdorda zarar yetkazib yoki uyushgan guruh tomonidan",
                "card_s": ["8–12 yil ozodlikdan mahrum qilish"],
                "cap_d": "juda ko‘p miqdorda zarar yetkazib, uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab",
                "cap_s": "8–12 yil ozodlikdan mahrum qilish",
            },
        ],
        "tip": "Davlat manfaatini shaxsiy manfaatdan ustun qo‘ying",
        "tip_pill": "Halol ishlang!",
    },
    {
        "n": 176, "slot": "1700", "title": "Qalbaki pul yasash", "tag": "qalbakipul", "emoji": "💵", "tip_emoji": "🔎",
        "hook": "Qalbaki pul yasash yoki uni muomalaga chiqarish — og‘ir jinoyat",
        "name_tts": "bir yuz yetmish oltinchi",
        "name_long": "qalbaki pul, aksiz markasi yoki qimmatli qog‘ozlar yasash, ularni o‘tkazish",
        "parts": [
            {
                "pill": "1-qism",
                "tts_d": "Qalbaki banknotlar, metall tangalar, aksiz markalari, qimmatli qog‘ozlar yoki chet el valyutasidagi qimmatli qog‘ozlarni o‘tkazish maqsadida yasash yoxud ularni o‘tkazish.",
                "tts_s": "ikki yildan besh yilgacha ozodlikni cheklash yoki besh yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Qalbaki pul, tanga, aksiz markasi yoki qimmatli qog‘oz yasash yoki o‘tkazish",
                "card_s": ["2–5 yil ozodlikni cheklash", "yoki 5 yilgacha ozodlikdan mahrum qilish"],
                "cap_d": "qalbaki banknot, metall tanga, aksiz markasi, qimmatli qog‘oz yoki chet el valyutasidagi qimmatli qog‘ozni o‘tkazish maqsadida yasash yoki o‘tkazish",
                "cap_s": "2–5 yil ozodlikni cheklash yoki 5 yilgacha ozodlikdan mahrum qilish",
            },
            {
                "pill": "2-qism",
                "tts_d": "Takroran yoki xavfli retsidivist tomonidan, ko‘p miqdorda, yoxud bir guruh shaxslar tomonidan oldindan til biriktirib sodir etilsa.",
                "tts_s": "besh yildan o‘n yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Takroran, ko‘p miqdorda yoki oldindan til biriktirgan guruh tomonidan",
                "card_s": ["5–10 yil ozodlikdan mahrum qilish"],
                "cap_d": "takroran yoki xavfli retsidivist tomonidan, ko‘p miqdorda, bir guruh shaxslar tomonidan oldindan til biriktirib",
                "cap_s": "5–10 yil ozodlikdan mahrum qilish",
            },
            {
                "pill": "3-qism",
                "tts_d": "Juda ko‘p miqdorda, yoxud uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab sodir etilsa.",
                "tts_s": "o‘n yildan o‘n besh yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Juda ko‘p miqdorda yoki uyushgan guruh tomonidan",
                "card_s": ["10–15 yil ozodlikdan mahrum qilish"],
                "cap_d": "juda ko‘p miqdorda, uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab",
                "cap_s": "10–15 yil ozodlikdan mahrum qilish",
            },
        ],
        "tip": "Shubhali pulni ko‘rsangiz, bankka yoki huquqni muhofaza qiluvchi organlarga xabar bering",
        "tip_pill": "Hushyor bo‘ling!",
    },
    {
        "n": 177, "slot": "1705", "title": "Valyutani noqonuniy olish", "tag": "valyuta", "emoji": "💱", "tip_emoji": "🏦",
        "hook": "Valyuta, oltin yoki qimmatbaho toshni qonunga xilof olish-sotish — jinoyat",
        "name_tts": "bir yuz yetmish yettinchi",
        "name_long": "valyuta qimmatliklarini, qimmatbaho metallar va (yoki) qimmatbaho toshlarni qonunga xilof ravishda olish yoki o‘tkazish",
        "parts": [
            {
                "pill": "1-qism",
                "tts_d": "Shunday qilmish uchun ma’muriy jazo qo‘llanilganidan keyin valyuta qimmatliklari, qimmatbaho metallar yoki qimmatbaho toshlarni qonunga xilof ravishda olish yoki o‘tkazish.",
                "tts_s": "yetmish besh baravaridan yuz baravarigacha bazaviy hisoblash miqdorida jarima, ikki yildan uch yilgacha axloq tuzatish ishlari, bir yilgacha ozodlikni cheklash yoki bir yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Ma’muriy jazodan keyin valyuta, qimmatbaho metall yoki toshni qonunga xilof olish yoki o‘tkazish",
                "card_s": ["75–100 BHM jarima …", "1 yilgacha ozodlikni cheklash", "yoki 1 yilgacha ozodlikdan mahrum qilish"],
                "cap_d": "shunday qilmish uchun ma’muriy jazo qo‘llanilganidan keyin valyuta qimmatliklari, qimmatbaho metallar yoki qimmatbaho toshlarni qonunga xilof ravishda olish yoki o‘tkazish",
                "cap_s": "75–100 BHM jarima, 2–3 yil axloq tuzatish ishlari, 1 yilgacha ozodlikni cheklash yoki 1 yilgacha ozodlikdan mahrum qilish",
            },
            {
                "pill": "2-qism",
                "tts_d": "O‘sha harakatlar ancha miqdorda sodir etilsa.",
                "tts_s": "yuz baravaridan uch yuz baravarigacha bazaviy hisoblash miqdorida jarima, bir yildan uch yilgacha ozodlikni cheklash yoki bir yildan uch yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Ancha miqdorda",
                "card_s": ["100–300 BHM jarima", "yoki 1–3 yil ozodlikni cheklash", "yoki 1–3 yil ozodlikdan mahrum qilish"],
                "cap_d": "ancha miqdorda",
                "cap_s": "100–300 BHM jarima, 1–3 yil ozodlikni cheklash yoki 1–3 yil ozodlikdan mahrum qilish",
            },
            {
                "pill": "3-qism",
                "tts_d": "Takroran yoki xavfli retsidivist tomonidan, ko‘p miqdorda, yoxud bir guruh shaxslar tomonidan oldindan til biriktirib sodir etilsa.",
                "tts_s": "uch yuz baravaridan besh yuz baravarigacha bazaviy hisoblash miqdorida jarima, uch yildan besh yilgacha ozodlikni cheklash yoki uch yildan besh yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Takroran, ko‘p miqdorda yoki oldindan til biriktirgan guruh tomonidan",
                "card_s": ["300–500 BHM jarima", "yoki 3–5 yil ozodlikni cheklash", "yoki 3–5 yil ozodlikdan mahrum qilish"],
                "cap_d": "takroran yoki xavfli retsidivist tomonidan, ko‘p miqdorda, bir guruh shaxslar tomonidan oldindan til biriktirib",
                "cap_s": "300–500 BHM jarima, 3–5 yil ozodlikni cheklash yoki 3–5 yil ozodlikdan mahrum qilish",
            },
            {
                "pill": "4-qism",
                "tts_d": "Juda ko‘p miqdorda, yoxud uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab sodir etilsa.",
                "tts_s": "besh yildan yetti yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Juda ko‘p miqdorda yoki uyushgan guruh tomonidan",
                "card_s": ["5–7 yil ozodlikdan mahrum qilish"],
                "cap_d": "juda ko‘p miqdorda, uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab",
                "cap_s": "5–7 yil ozodlikdan mahrum qilish",
            },
        ],
        "tip": "Valyuta va oltinni faqat bank va rasmiy shoxobchalar orqali oling",
        "tip_pill": "Qonuniy yo‘lni tanlang!",
    },
    {
        "n": 178, "slot": "2100", "title": "Valyutani yashirish", "tag": "valyutaniyashirish", "emoji": "🙈", "tip_emoji": "✅",
        "hook": "Bankka o‘tkazilishi shart bo‘lgan valyutani yashirish — jinoyat",
        "name_tts": "bir yuz yetmish sakkizinchi",
        "name_long": "chet el valyutasini yashirish",
        "parts": [
            {
                "pill": "1-qism",
                "tts_d": "Korxona, muassasa yoki tashkilotlarda valyuta operatsiyalari bilan shug‘ullanuvchi xodimlar tomonidan O‘zbekistonning vakolatli banklaridagi hisob raqamlarga o‘tkazilishi lozim bo‘lgan chet el valyutasini qasddan yashirish.",
                "tts_s": "yetmish besh baravaridan yuz baravarigacha bazaviy hisoblash miqdorida jarima, uch yildan besh yilgacha muayyan huquqdan mahrum qilish, ikki yildan besh yilgacha ozodlikni cheklash yoki besh yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Vakolatli bankka o‘tkazilishi lozim bo‘lgan chet el valyutasini qasddan yashirish",
                "card_s": ["75–100 BHM jarima …", "2–5 yil ozodlikni cheklash", "yoki 5 yilgacha ozodlikdan mahrum qilish"],
                "cap_d": "valyuta operatsiyalari bilan shug‘ullanuvchi xodimlar tomonidan vakolatli banklardagi hisob raqamlarga o‘tkazilishi lozim bo‘lgan chet el valyutasini qasddan yashirish",
                "cap_s": "75–100 BHM jarima, 3–5 yil muayyan huquqdan mahrum qilish, 2–5 yil ozodlikni cheklash yoki 5 yilgacha ozodlikdan mahrum qilish",
            },
            {
                "pill": "2-qism",
                "tts_d": "G‘arazgo‘ylik bilan, takroran, yoxud bir guruh shaxslar tomonidan oldindan til biriktirib sodir etilsa.",
                "tts_s": "besh yildan sakkiz yilgacha ozodlikdan mahrum qilish.",
                "card_d": "G‘arazgo‘ylik bilan, takroran yoki oldindan til biriktirgan guruh tomonidan",
                "card_s": ["5–8 yil ozodlikdan mahrum qilish"],
                "cap_d": "g‘arazgo‘ylik bilan, takroran yoki bir guruh shaxslar tomonidan oldindan til biriktirib",
                "cap_s": "5–8 yil ozodlikdan mahrum qilish",
            },
            {
                "pill": "3-qism",
                "tts_d": "Uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab sodir etilsa.",
                "tts_s": "sakkiz yildan o‘n ikki yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab",
                "card_s": ["8–12 yil ozodlikdan mahrum qilish"],
                "cap_d": "uyushgan guruh tomonidan yoki uning manfaatlarini ko‘zlab",
                "cap_s": "8–12 yil ozodlikdan mahrum qilish",
            },
        ],
        "tip": "Valyuta tushumini o‘z vaqtida bankka o‘tkazing",
        "tip_pill": "Qonunga amal qiling!",
    },
    {
        "n": 179, "slot": "2105", "title": "Soxta tadbirkorlik", "tag": "soxtatadbirkorlik", "emoji": "🏚️", "tip_emoji": "💼",
        "hook": "Faqat kredit olish yoki soliqdan qochish uchun firma ochish — soxta tadbirkorlik",
        "name_tts": "bir yuz yetmish to‘qqizinchi",
        "name_long": "soxta tadbirkorlik",
        "parts": [
            {
                "pill": "Modda mazmuni",
                "tts_d": "Tadbirkorlik faoliyatini amalga oshirish niyati bo‘lmagan holda, kredit yoki qarz olish, soliqlarni kamaytirish yoki ulardan bo‘yin tovlash yoxud boshqa mulkiy naf ko‘rish maqsadida xo‘jalik yurituvchi subyekt tashkil etish.",
                "tts_s": "yuz baravaridan ikki yuz baravarigacha bazaviy hisoblash miqdorida jarima, uch yilgacha axloq tuzatish ishlari yoxud muayyan huquqdan mahrum qilib, bir yildan uch yilgacha ozodlikni cheklash yoki bir yildan uch yilgacha ozodlikdan mahrum qilish.",
                "card_d": "Biznes qilish niyatisiz — kredit olish yoki soliqdan qochish uchun firma ochish",
                "card_s": ["100–200 BHM jarima …", "1–3 yil ozodlikni cheklash", "yoki 1–3 yil ozodlikdan mahrum qilish"],
                "cap_d": "tadbirkorlik niyatisiz kredit yoki qarz olish, soliqlarni kamaytirish yoki ulardan bo‘yin tovlash yoxud boshqa mulkiy naf ko‘rish uchun xo‘jalik yurituvchi subyekt tashkil etish",
                "cap_s": "100–200 BHM jarima, 3 yilgacha axloq tuzatish ishlari yoki muayyan huquqdan mahrum qilib 1–3 yil ozodlikni cheklash yoki 1–3 yil ozodlikdan mahrum qilish",
                "cap_label": "Modda",
            },
        ],
        "tip": "Biznesni halol yuriting, soliqni to‘g‘ri to‘lang",
        "tip_pill": "Halol biznes!",
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
