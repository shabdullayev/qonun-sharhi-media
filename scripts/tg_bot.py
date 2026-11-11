"""Qonun sharhi — Telegram kanal avtomati (GitHub Actions'da ishlaydi).

1) Videolar: queue/telegram_queue.json dagi vaqti kelgan videolarni kanalga yuboradi.
2) Yangiliklar: Kun.uz, Daryo.uz, Qalampir.uz lentalaridan qonunchilikka oid yangiliklarni topib,
   sarlavha + qisqa mazmun + manba havolasi bilan yuboradi (maqola to‘liq ko‘chirilmaydi).
Maxfiy ma’lumotlar faqat GitHub secrets'da: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.
Secrets bo‘lmasa — "quruq" rejim: hech narsa yubormaydi, faqat topilganini chiqaradi."""
import datetime as dt, email.utils, html, json, os, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = dt.timezone(dt.timedelta(hours=5))
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
DRY = not (TOKEN and CHAT) or os.environ.get("DRY_RUN") == "1"
UA = {"User-Agent": "Mozilla/5.0 (QonunSharhiBot; +https://github.com/shabdullayev/qonun-sharhi-media)"}
NOW = dt.datetime.now(TZ)

FEEDS = [
    ("Kun.uz", ["https://kun.uz/news/rss", "https://kun.uz/uz/news/rss"]),
    ("Daryo.uz", ["https://daryo.uz/rss", "https://daryo.uz/feed"]),
    ("Qalampir.uz", ["html:https://qalampir.uz/uz/latest"]),
]
NEWALPHA = str.maketrans({"ö": "o‘", "Ö": "O‘", "ğ": "g‘", "Ğ": "G‘", "ş": "sh", "Ş": "Sh", "ç": "ch", "Ç": "Ch"})
# qonunchilik belgilari (lotin + kirill); jinoyat xronikasi emas, qonun/qaror/tartib o‘zgarishi
LAW = re.compile(
    r"qonun|kodeks|farmon|prezident qarori|vazirlar mahkamasi|oliy majlis|senat|qonunchilik palatasi|"
    r"kuchga kir|imzoladi|o[‘'ʻ`]?zgartirish|tuzatish kirit|yangi tartib|tartib o[‘'ʻ`]?zgar|jarima miqdori|"
    r"bhm|bazaviy hisoblash|konstitutsiya|loyiha muhokama|regulation\.gov|lex\.uz|"
    r"закон|кодекс|фармон|қарор|указ|постановлени|олий мажлис|сенат|қонунчилик палатаси|кучга кир|"
    r"имзолади|ўзгартириш|янги тартиб|жарима миқдори|бҳм|конституция",
    re.I)
NOISE = re.compile(r"futbol|chempionat|kino|konsert|ob-havo|футбол|чемпионат|концерт|об-ҳаво|погода", re.I)


def tg(method, data):
    if DRY:
        print("[DRY]", method, {k: (v[:80] if isinstance(v, str) else v) for k, v in data.items()})
        return {"ok": True, "result": {"message_id": 0}}
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/{method}",
                                 data=urllib.parse.urlencode(data).encode(), method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def load(path, default):
    p = os.path.join(ROOT, path)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return default


def save(path, obj):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ videos
def run_videos():
    q = load("queue/telegram_queue.json", {"items": []})
    sent = 0
    last = q.get("last_sent")
    if last and (NOW - dt.datetime.fromisoformat(last)).total_seconds() < 28 * 60:
        print("videos: last one was under 30 min ago")
        return
    for it in sorted(q["items"], key=lambda x: x["due"]):
        if it.get("status") != "pending":
            continue
        due = dt.datetime.fromisoformat(it["due"])
        if due > NOW or sent >= 1:   # bir ishga tushishda bitta video, oraliq kamida 30 daqiqa
            continue
        cap = it.get("caption", "")
        if len(cap) > 1024:
            cap = cap[:1000].rsplit("\n", 1)[0] + "\n…"
        try:
            r = tg("sendVideo", {"chat_id": CHAT, "video": it["url"], "caption": cap, "supports_streaming": "true"})
        except Exception as e:  # noqa
            print("video error", it.get("id"), e)
            it["error"] = str(e)[:200]
            continue
        if r.get("ok"):
            if not DRY:
                q["last_sent"] = NOW.isoformat(timespec="seconds")
                it["status"] = "sent"
                it["sent_at"] = NOW.isoformat(timespec="seconds")
                it["message_id"] = r["result"]["message_id"]
            sent += 1
            print("video sent", it.get("id"))
        else:
            print("video failed", it.get("id"), r)
            it["error"] = str(r)[:200]
    save("queue/telegram_queue.json", q)


# ------------------------------------------------------------------ news
def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def strip(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def parse(raw):
    items = []
    root = ET.fromstring(raw)
    for it in root.iter("item"):
        g = lambda t: (it.findtext(t) or "").strip()  # noqa
        when = None
        if g("pubDate"):
            try:
                when = email.utils.parsedate_to_datetime(g("pubDate"))
            except Exception:  # noqa
                when = None
        items.append({"title": strip(g("title")), "link": g("link"), "desc": strip(g("description")), "when": when})
    return items


def parse_html(raw, base):
    items, ids = [], set()
    txt = raw.decode("utf-8", "ignore")
    for m in re.finditer(r'<a[^>]+href="(/uz/news/[^"]+)"[^>]*>(.*?)</a>', txt, re.S):
        href, title = m.group(1), strip(m.group(2))
        title = re.sub(r"\s*visibility\s*\d+.*$", "", title)
        title = re.sub(r"\s*\d{1,2}:\d{2}\s*$", "", title)
        title = re.sub(r"\s*\d{1,2} (Yanvar|Fevral|Mart|Aprel|May|Iyun|Iyul|Avgust|Sentabr|Oktabr|Noyabr|Dekabr)\s*$", "", title)
        if len(title) < 15 or href in ids:
            continue
        ids.add(href)
        items.append({"title": title, "link": base + href, "desc": "", "when": None})
    return items


def run_news():
    seen = load("queue/telegram_news_seen.json", None)
    first = seen is None
    seen = seen or {"links": []}
    seen.setdefault("seeded", [s for s, _ in FEEDS if not first and s != "Qalampir.uz"])
    known = set(seen["links"])
    posted = 0
    for source, urls in FEEDS:
        items = None
        seeding = first or source not in seen["seeded"]
        for u in urls:
            try:
                if u.startswith("html:"):
                    u = u[5:]
                    items = parse_html(fetch(u), "https://qalampir.uz")
                else:
                    items = parse(fetch(u))
                print(source, "ok", u, len(items))
                break
            except Exception as e:  # noqa
                print(source, "fail", u, str(e)[:120])
        if not items:
            continue
        for n in items:
            if not n["link"] or n["link"] in known:
                continue
            known.add(n["link"])
            seen["links"].append(n["link"])
            n["title"] = n["title"].translate(NEWALPHA)
            n["desc"] = n["desc"].translate(NEWALPHA)
            text = n["title"] + " " + n["desc"]
            if seeding or not LAW.search(text) or NOISE.search(n["title"]):
                continue
            if n["when"] and (NOW - n["when"]).total_seconds() > 6 * 3600:
                continue
            if posted >= 4:
                continue
            desc = n["desc"]
            if len(desc) > 280:
                desc = desc[:280].rsplit(" ", 1)[0] + "…"
            msg = (f"⚖️ <b>{html.escape(n['title'])}</b>\n\n" + (html.escape(desc) + "\n\n" if desc else "") +
                   f"🔗 Batafsil: <a href=\"{html.escape(n['link'])}\">{source}</a>\n\n#qonunchilik #yangilik")
            try:
                r = tg("sendMessage", {"chat_id": CHAT, "text": msg, "parse_mode": "HTML",
                                       "disable_web_page_preview": "false"})
                print("news", "ok" if r.get("ok") else r, n["title"][:70])
                posted += 1
                time.sleep(2)
            except Exception as e:  # noqa
                print("news error", e)
        if seeding and source not in seen["seeded"]:
            seen["seeded"].append(source)
            print(source, "seeded: current items marked as seen")
    seen["links"] = seen["links"][-1500:]
    save("queue/telegram_news_seen.json", seen)
    if first:
        print("first run: current items marked as seen, nothing posted")


if __name__ == "__main__":
    print("now", NOW.isoformat(), "DRY" if DRY else "LIVE")
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "videos"):
        run_videos()
    if what in ("all", "news"):
        run_news()
