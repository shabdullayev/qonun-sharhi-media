"""Qonun sharhi — Telegram kanal avtomati (GitHub Actions'da ishlaydi).

1) Videolar: queue/telegram_queue.json dagi vaqti kelgan videolarni kanalga yuboradi
   (oraliq kamida 30 daqiqa; ish jarayoni navbatdagi video vaqtigacha kutib turadi).
2) Yangiliklar: Kun.uz, Daryo.uz, Qalampir.uz, Advice.uz, Norma.uz, Yuridikmaslahat.uz dan qonunchilikka oid yangiliklarni topib,
   sarlavha + qisqa mazmun + manba havolasi bilan yuboradi (maqola to‘liq ko‘chirilmaydi).
Har bir post oxiriga kanal belgisi (SIGNATURE, odatda @huquq_ustuvor) qo‘shiladi.
Maxfiy ma’lumotlar faqat GitHub secrets'da: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.
Secrets bo‘lmasa — "quruq" rejim: hech narsa yubormaydi, faqat topilganini chiqaradi.

Rejimlar: all | videos | news | check | probe | sign | delete
"""
import datetime as dt, email.utils, html, json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = dt.timezone(dt.timedelta(hours=5))
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
DRY = not (TOKEN and CHAT) or os.environ.get("DRY_RUN") == "1"
SIGN = os.environ.get("SIGNATURE", "@huquq_ustuvor").strip()
LOOP_MIN = int(os.environ.get("LOOP_MINUTES", "0") or 0)
IN_CI = os.environ.get("GITHUB_ACTIONS") == "true"
UA = {"User-Agent": "Mozilla/5.0 (QonunSharhiBot; +https://github.com/shabdullayev/qonun-sharhi-media)"}
QF, SF = "queue/telegram_queue.json", "queue/telegram_news_seen.json"
GAP = dt.timedelta(minutes=29, seconds=30)      # videolar orasidagi eng kam oraliq
NEWS_EVERY = dt.timedelta(minutes=10)


def now():
    return dt.datetime.now(TZ)


# source, urls; "html:<url>|<href regex>|<base>" — RSS bo‘lmagan saytlar; all_law=True — bo‘limning hammasi qonunchilik
FEEDS = [
    ("Kun.uz", ["https://kun.uz/news/rss", "https://kun.uz/uz/news/rss"], False),
    ("Daryo.uz", ["https://daryo.uz/rss", "https://daryo.uz/feed"], False),
    ("Qalampir.uz", [r"html:https://qalampir.uz/uz/latest|(/uz/news/[^\"#?]+)|https://qalampir.uz"], False),
    ("Advice.uz", [r"html:https://www.advice.uz/oz/category/784|((?:https?://(?:www\.)?advice\.uz)?/oz/document/\d+)|https://www.advice.uz"], True),
    # Norma.uz: bosh sahifadagi "Новое в законодательстве" ro‘yxati (RSS bo‘sh; /ru/ sahifalarini o‘qimaymiz — robots.txt)
    ("Norma.uz", [r"html:https://www.norma.uz/|(/ru/novoe_v_zakonodatelstve/[^\"#?]+)|https://www.norma.uz"], True),
    # Yuridikmaslahat.uz: "Maqolalar" (RSS yo‘q); sarlavha kartochkadagi <p> ichida
    ("Yuridikmaslahat.uz", [r"html:https://yuridikmaslahat.uz/maqolalar|(/maqolalar/[a-z0-9-]+)|https://yuridikmaslahat.uz|p"], True),
]
NEWALPHA = str.maketrans({"ö": "o‘", "Ö": "O‘", "ğ": "g‘", "Ğ": "G‘", "ş": "sh", "Ş": "Sh", "ç": "ch", "Ç": "Ch"})
A = r"[‘'ʻ`’]?"   # o‘ / g‘ belgisi variantlari
# qonunchilik belgilari: qonun/kodeks/farmon/qaror, kuchga kirish — jinoyat xronikasi yoki umumiy siyosat emas
LAW = re.compile(
    r"(?<!no)qonun(?!buzar|siz)|kodeks|farmon|prezident qarori|hukumat qarori|vazirlar mahkamasi|oliy majlis|senat|"
    r"qonunchilik palatasi|konstitutsiya|kuchga kir|normativ-huquqiy|lex\.uz|regulation\.gov|"
    r"(?<!но)қонун(?!бузар|сиз)|(?<!не)закон|кодекс|фармон|президент қарори|вазирлар маҳкамаси|олий мажлис|"
    r"сенат|қонунчилик палатаси|конституци|кучга кир|вступ\w* в силу|указ президента|постановлени\w* президента",
    re.I)
# xorijiy mavzu (sarlavhada) — O‘zbekiston tilga olinmasa o‘tkazib yuboriladi
FOREIGN = re.compile(
    rf"\b(?:aqsh|amerika|rossiya|ukraina|xitoy|yevropa|yevroittifoq|isroil|eron|g{A}azo|falastin|tramp|putin|zelenskiy|"
    rf"germaniya|fransiya|britaniya|turkiya|qozog{A}iston|qirg{A}iziston|tojikiston|turkmaniston|afg{A}oniston|"
    rf"hindiston|pokiston|yaponiya|koreya|nato|bmt|kreml|vashington|moskva|kiyev|kongress|"
    r"сша|америк|росси|украин|хитой|китай|европ|исроил|израил|эрон|иран|газа|трамп|путин|зеленск|германи|франци|"
    r"британи|туркия|турци|қозоғистон|казахстан|қирғизистон|киргиз|тожикистон|таджик|афғонистон|афганистан|"
    r"ҳиндистон|индия|покистон|пакистан|япони|корея|нато|бмт|оон|кремл|вашингтон|москв|киев|конгресс)",
    re.I)
UZ = re.compile(rf"o{A}zbekiston|mirziyoyev|toshkent|oliy majlis|qonunchilik palatasi|vazirlar mahkamasi|lex\.uz|"
                r"ўзбекистон|узбекистан|мирзиёев|тошкент|ташкент|олий мажлис|қонунчилик палатаси", re.I)
NOISE = re.compile(r"futbol|chempionat|kino|konsert|ob-havo|футбол|чемпионат|концерт|об-ҳаво|погода", re.I)

# --------------------------------------------------------------- xotiradagi o‘zgarishlar (git bilan sinxron)
ITEM_UPD = {}      # video id -> yangilanadigan maydonlar
LAST_SENT = None
NEW_LINKS, SEEDED, POSTED = [], [], []
MAXID = {}         # manba -> ko‘rilgan eng katta hujjat raqami (advice.uz)


def tg(method, data):
    if DRY:
        print("[DRY]", method, {k: (v[:80] if isinstance(v, str) else v) for k, v in data.items()})
        return {"ok": True, "result": {"message_id": 0}}
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/{method}",
                                 data=urllib.parse.urlencode(data).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:  # Telegram xatosi matnini qaytaramiz (token chiqmaydi)
        try:
            return json.loads(e.read().decode("utf-8", "replace"))
        except Exception:  # noqa
            return {"ok": False, "description": f"HTTP {e.code}"}


def load(path, default):
    p = os.path.join(ROOT, path)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return default


def save(path, obj):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def apply_changes():
    q = load(QF, {"items": []})
    for it in q.get("items", []):
        if it.get("id") in ITEM_UPD:
            it.update(ITEM_UPD[it["id"]])
    if LAST_SENT and (not q.get("last_sent") or q["last_sent"] < LAST_SENT):
        q["last_sent"] = LAST_SENT
    save(QF, q)
    s = load(SF, None) or {"links": []}
    links = s.setdefault("links", [])
    known = set(links)
    for l in NEW_LINKS:
        if l not in known:
            links.append(l)
            known.add(l)
    s["links"] = links[-2000:]
    seeded = s.setdefault("seeded", [])
    for x in SEEDED:
        if x not in seeded:
            seeded.append(x)
    posted = s.setdefault("posted", [])
    ids = {p.get("message_id") for p in posted}
    for p in POSTED:
        if p["message_id"] not in ids:
            posted.append(p)
    s["posted"] = posted[-300:]
    mx = s.setdefault("maxid", {})
    for k, v in MAXID.items():
        mx[k] = max(v, mx.get(k, 0))
    save(SF, s)


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def sync():
    """Masofadagi oxirgi holatni olib, o‘zgarishlarni ustiga qo‘yadi va push qiladi (takror yuborishning oldini oladi)."""
    if not IN_CI:
        apply_changes()
        return True
    for attempt in range(6):
        r = git("fetch", "-q", "origin", "main")
        if r.returncode:
            print("git fetch xato:", r.stderr[:200])
            time.sleep(4)
            continue
        git("reset", "-q", "--hard", "origin/main")
        apply_changes()
        git("add", QF, SF)
        if git("diff", "--cached", "--quiet").returncode == 0:
            return True
        git("-c", "user.name=qonun-sharhi-bot", "-c", "user.email=actions@users.noreply.github.com",
            "commit", "-q", "-m", "Telegram holati yangilandi [skip ci]")
        r = git("push", "-q", "origin", "HEAD:main")
        if r.returncode == 0:
            return True
        print("git push qayta urinish:", r.stderr[:200])
        time.sleep(4)
    print("sync: holatni saqlab bo‘lmadi")
    return False


def with_sign(text, limit):
    if not SIGN or SIGN in text:
        return text[:limit]
    tail = "\n\n" + SIGN
    room = limit - len(tail)
    if len(text) > room:
        text = text[:room - 2].rsplit("\n", 1)[0] + "\n…"
    return text + tail


# ------------------------------------------------------------------ videos
def next_video_time(q):
    last = q.get("last_sent")
    floor = dt.datetime.fromisoformat(last) + GAP if last else None
    best = None
    for it in q.get("items", []):
        if it.get("status") != "pending":
            continue
        t = dt.datetime.fromisoformat(it["due"])
        if floor and t < floor:
            t = floor
        if it.get("retry_after"):
            t = max(t, dt.datetime.fromisoformat(it["retry_after"]))
        best = t if best is None or t < best else best
    return best


def run_videos():
    """Vaqti kelgan bitta videoni yuboradi (oraliq kamida 30 daqiqa)."""
    global LAST_SENT
    q = load(QF, {"items": []})
    t = next_video_time(q)
    if t is None or t > now():
        return False
    for it in sorted(q["items"], key=lambda x: x["due"]):
        if it.get("status") != "pending":
            continue
        if dt.datetime.fromisoformat(it["due"]) > now():
            break
        if it.get("retry_after") and dt.datetime.fromisoformat(it["retry_after"]) > now():
            continue
        cap = with_sign(it.get("caption", ""), 1024)
        r = tg("sendVideo", {"chat_id": CHAT, "video": it["url"], "caption": cap, "supports_streaming": "true"})
        ts = now().isoformat(timespec="seconds")
        if r.get("ok"):
            print("video sent", it["id"], "message", r["result"].get("message_id"))
            if not DRY:
                LAST_SENT = ts
                ITEM_UPD[it["id"]] = {"status": "sent", "sent_at": ts, "message_id": r["result"]["message_id"],
                                      "signed": bool(SIGN), "error": None, "retry_after": None}
                apply_changes()
            return True
        fails = int(it.get("fails", 0)) + 1
        print("video failed", it["id"], r.get("description"))
        upd = {"fails": fails, "error": str(r.get("description"))[:200],
               "retry_after": (now() + dt.timedelta(minutes=10)).isoformat(timespec="seconds")}
        if fails >= 3:
            upd["status"] = "failed"
        ITEM_UPD[it["id"]] = upd
        apply_changes()
        return False
    return False


# ------------------------------------------------------------------ news
def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def strip(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s).replace("\u00ad", "").replace("\u200b", "")
    return re.sub(r"\s+", " ", s).strip()


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


MONTHS = r"(Yanvar|Fevral|Mart|Aprel|May|Iyun|Iyul|Avgust|Sentabr|Oktabr|Noyabr|Dekabr)"


def uzq(t):
    """o' / g' va boshqa apostroflarni joriy lotin yozuvidagi o‘, g‘ va ’ belgilariga keltiradi."""
    t = t.replace("ʻ", "‘").replace("ʼ", "’")
    t = re.sub(r"([OoGg])[\'`’]", r"\1‘", t)
    return t.replace("'", "’")


def parse_html(raw, href_re, base, mode=""):
    items, ids = [], set()
    txt = raw.decode("utf-8", "ignore")
    for m in re.finditer(r'<a[^>]+href="' + href_re + r'"[^>]*>(.*?)</a>', txt, re.S | re.I):
        href, inner = m.group(1), m.group(2)
        pm = re.search(r"<p(?:\s[^>]*)?>(.*?)</p>", inner, re.S | re.I) if mode == "p" else None
        title = strip(pm.group(1)) if pm else strip(inner)
        title = re.sub(r"\s*visibility\s*\d+.*$", "", title)
        title = re.sub(r"\s*\d{1,2}:\d{2}\s*$", "", title)
        title = re.sub(r"\s*\d{1,2} " + MONTHS + r"\s*$", "", title)
        title = re.sub(r"^\s*\d{2}\.\d{2}\.\d{2}(?:\d{2})?\s*", "", title)
        title = re.sub(r"\s*\d{2}\.\d{2}\.\d{2}(?:\d{2})?\s*$", "", title)
        link = href if href.startswith("http") else base + href
        if len(title) < 15 or link in ids:
            continue
        ids.add(link)
        items.append({"title": title, "link": link, "desc": "", "when": None})
    return items


def get_items(urls):
    out, ok = [], False
    for u in urls:
        try:
            if u.startswith("html:"):
                page, href_re, base, *opt = u[5:].split("|")
                its = parse_html(fetch(page), href_re, base, opt[0] if opt else "")
                print("  ok", page, len(its))
            else:
                its = parse(fetch(u))
                print("  ok", u, len(its))
            ok = True
            have = {x["link"] for x in out}
            out += [x for x in its if x["link"] not in have]
            if not u.startswith("html:"):
                break       # RSS: birinchi ishlagani yetarli
        except Exception as e:  # noqa
            print("  fail", u.split("|")[0], str(e)[:120])
    return out if ok else None


def is_law(n, all_law):
    title, text = n["title"], n["title"] + " " + n["desc"]
    if NOISE.search(title):
        return False
    if FOREIGN.search(title) and not UZ.search(text):
        return False
    return all_law or bool(LAW.search(text))


def doc_id(link):
    m = re.search(r"/document/(\d+)", link)
    return int(m.group(1)) if m else None


def run_news(probe=False):
    s = load(SF, None)
    first = s is None
    s = s or {"links": []}
    seeded = set(s.get("seeded", [])) | set(SEEDED)
    known = set(s.get("links", [])) | set(NEW_LINKS)
    maxid = dict(s.get("maxid", {}))
    maxid.update({k: max(v, maxid.get(k, 0)) for k, v in MAXID.items()})
    posted = 0
    for source, urls, all_law in FEEDS:
        print(source)
        items = get_items(urls)
        if not items:
            continue
        if probe:
            show = items[:8] + ([None] + items[-6:] if len(items) > 14 else [])
            for n in show:
                if n is None:
                    print("    ..."); continue
                n = dict(n, title=uzq(n["title"].translate(NEWALPHA)), desc=uzq(n["desc"].translate(NEWALPHA)))
                print("   ", "LAW" if is_law(n, all_law) else "---", n["title"][:90], "|", n["link"])
            continue
        seeding = first or source not in seeded
        ids = [doc_id(n["link"]) for n in items if doc_id(n["link"])]
        for n in items:
            if not n["link"] or n["link"] in known:
                continue
            known.add(n["link"])
            NEW_LINKS.append(n["link"])
            n["title"] = uzq(n["title"].translate(NEWALPHA))
            n["desc"] = uzq(n["desc"].translate(NEWALPHA))
            did = doc_id(n["link"])
            if did and maxid.get(source) and did <= maxid[source]:
                continue          # eski hujjat (ro‘yxatda qayta chiqqan)
            if seeding or not is_law(n, all_law):
                continue
            if n["when"] and (now() - n["when"]).total_seconds() > 6 * 3600:
                continue
            if posted >= 4:
                continue
            desc = n["desc"]
            if len(desc) > 280:
                desc = desc[:280].rsplit(" ", 1)[0] + "…"
            msg = (f"⚖️ <b>{html.escape(n['title'])}</b>\n\n" + (html.escape(desc) + "\n\n" if desc else "") +
                   f"🔗 Batafsil: <a href=\"{html.escape(n['link'])}\">{source}</a>\n\n#qonunchilik #yangilik" +
                   (f"\n\n{html.escape(SIGN)}" if SIGN else ""))
            r = tg("sendMessage", {"chat_id": CHAT, "text": msg, "parse_mode": "HTML",
                                   "disable_web_page_preview": "false"})
            if r.get("ok"):
                mid = r["result"].get("message_id")
                print("  news sent", mid, n["title"][:70])
                if not DRY:
                    POSTED.append({"message_id": mid, "title": n["title"][:120], "link": n["link"],
                                   "at": now().isoformat(timespec="seconds")})
                posted += 1
                time.sleep(2)
            else:
                print("  news failed", r.get("description"), n["title"][:70])
        if ids:
            MAXID[source] = max(ids + [maxid.get(source, 0)])
        if seeding and source not in seeded:
            SEEDED.append(source)
            print("  seeded: current items marked as seen")
    if not probe:
        apply_changes()


# ------------------------------------------------------------------ boshqa rejimlar
def run_check():
    """Hech narsa joylamaydi: bot, kanal va botning admin huquqlarini tekshiradi."""
    if not (TOKEN and CHAT):
        print("CHECK: secrets yo‘q —", "TELEGRAM_BOT_TOKEN" if not TOKEN else "", "TELEGRAM_CHAT_ID" if not CHAT else "")
        return
    me = tg("getMe", {})
    if not me.get("ok"):
        print("CHECK getMe XATO:", me.get("description"))
        return
    bot = me["result"]
    print("CHECK bot: @%s (id %s)" % (bot.get("username"), bot.get("id")))
    ch = tg("getChat", {"chat_id": CHAT})
    if not ch.get("ok"):
        print("CHECK getChat XATO:", ch.get("description"))
        return
    c = ch["result"]
    print("CHECK kanal:", c.get("title"), "| type:", c.get("type"))
    m = tg("getChatMember", {"chat_id": CHAT, "user_id": bot["id"]})
    if not m.get("ok"):
        print("CHECK getChatMember XATO:", m.get("description"))
        return
    r = m["result"]
    print("CHECK bot holati:", r.get("status"), "| can_post_messages:", r.get("can_post_messages"),
          "| can_edit_messages:", r.get("can_edit_messages"), "| can_delete_messages:", r.get("can_delete_messages"))


def run_sign():
    """Yuborilgan, lekin kanal belgisi qo‘shilmagan video izohlariga belgini qo‘shadi."""
    q = load(QF, {"items": []})
    for it in q.get("items", []):
        if it.get("status") != "sent" or it.get("signed") or not it.get("message_id"):
            continue
        cap = with_sign(it.get("caption", ""), 1024)
        r = tg("editMessageCaption", {"chat_id": CHAT, "message_id": it["message_id"], "caption": cap})
        ok = r.get("ok") or "not modified" in str(r.get("description", ""))
        print("sign", it["id"], it["message_id"], "ok" if ok else r.get("description"))
        if ok and not DRY:
            ITEM_UPD[it["id"]] = {"signed": True}
    apply_changes()


def run_delete(mid):
    """Faqat botning o‘zi yuborgan xabarni o‘chiradi (avval egaligini tekshiradi)."""
    if not str(mid).isdigit():
        print("DELETE: message_id raqam bo‘lishi kerak")
        return
    r = tg("editMessageReplyMarkup", {"chat_id": CHAT, "message_id": mid})
    d = str(r.get("description", ""))
    if not (r.get("ok") or "not modified" in d):
        print("DELETE: bu xabar botniki emas yoki topilmadi —", d)
        return
    r = tg("deleteMessage", {"chat_id": CHAT, "message_id": mid})
    print("DELETE", mid, "ok" if r.get("ok") else r.get("description"))


def run_fetch(urls):
    """Diagnostika: berilgan sahifalarni ochib, holati, turi, RSS elementlari va havolalarini chiqaradi."""
    for u in [x.strip() for x in urls.split(",") if x.strip()]:
        raw_mode = u.startswith("raw:")
        u = u[4:] if raw_mode else u
        try:
            req = urllib.request.Request(u, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                raw, st, ct, fin = r.read(), r.status, r.headers.get("Content-Type"), r.geturl()
        except urllib.error.HTTPError as e:
            print("FETCH", u, "HTTP", e.code); continue
        except Exception as e:  # noqa
            print("FETCH", u, "xato", str(e)[:150]); continue
        txt = raw.decode("utf-8", "ignore")
        print("FETCH", u, st, ct, len(raw), "->", fin, "| <item>:", txt.count("<item"))
        if raw_mode:
            for m in list(re.finditer(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', txt, re.S | re.I))[:200]:
                if len(strip(m.group(2))) >= 25:
                    nodes = [strip(x) for x in re.split(r"<[^>]+>", m.group(2)) if strip(x)]
                    tags = re.findall(r"<(h[1-6]|p|span|div)[^>]*>([^<]{3,})", m.group(2))
                    print("    NODES", nodes)
                    print("    TAGS", [(t, strip(x)[:60]) for t, x in tags][:12]); break
            locs = re.findall(r"<loc>(.*?)</loc>(?:\s*<lastmod>(.*?)</lastmod>)?", txt)
            for l in locs[:12] + locs[-8:]:
                print("    LOC", l[0], l[1])
            print("    LOCS", len(locs))
            continue
        if u.endswith("robots.txt"):
            print("   ", txt[:600].replace("\n", " / ")); continue
        for m in re.finditer(r"<item>.*?<title>(.*?)</title>.*?<link>(.*?)</link>", txt, re.S):
            print("    RSS", strip(m.group(1))[:80], "|", m.group(2).strip()); 
        hrefs, seen = [], set()
        for m in re.finditer(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', txt, re.S | re.I):
            h, t = m.group(1), strip(m.group(2))
            if h in seen or len(t) < 12: continue
            seen.add(h); hrefs.append((h, t))
        for h, t in hrefs[:40]:
            print("    A", t[:80], "|", h)


CHAIN_H = float(os.environ.get("CHAIN_HOURS", "0") or 0)


def chain_next():
    """GitHub jadvali kechikadi: navbatda video bo‘lsa, keyingi ishga tushishni o‘zimiz chaqiramiz."""
    repo, tok = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_TOKEN")
    if DRY or not (IN_CI and repo and tok):
        print("chain: o‘tkazib yuborildi")
        return
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/actions/workflows/telegram.yml/dispatches",
                                 data=json.dumps({"ref": "main", "inputs": {"mode": "all"}}).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
                                          "Content-Type": "application/json", "User-Agent": "qonun-sharhi-bot"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("chain: keyingi ishga tushish chaqirildi", r.status)
    except urllib.error.HTTPError as e:
        print("chain: xato", e.code, e.read()[:200])
    except Exception as e:  # noqa
        print("chain: xato", str(e)[:200])


def run_all(videos=True, news=True):
    start = now()
    deadline = start + dt.timedelta(minutes=LOOP_MIN)
    last_news = None
    chain = False
    while True:
        sync()
        if videos:
            run_videos()
        if news and (last_news is None or now() - last_news >= NEWS_EVERY):
            run_news()
            last_news = now()
        sync()
        if LOOP_MIN <= 0 or not videos:
            break
        nxt = next_video_time(load(QF, {"items": []}))
        chain = bool(nxt and CHAIN_H > 0 and nxt - now() <= dt.timedelta(hours=CHAIN_H))
        if nxt is None or (nxt > deadline and not chain):
            print("loop: navbatdagi video", nxt.isoformat(timespec="minutes") if nxt else "yo‘q", "— tugatildi")
            break
        if now() >= deadline - dt.timedelta(seconds=20):
            break
        wake = min(nxt, (last_news or now()) + NEWS_EVERY, deadline)
        secs = max(15, (wake - now()).total_seconds())
        print("loop: kutish", int(secs), "s (navbatdagi video", nxt.strftime("%H:%M") + ")")
        time.sleep(secs)
    if chain:
        chain_next()


if __name__ == "__main__":
    print("now", now().isoformat(), "DRY" if DRY else "LIVE", "| loop", LOOP_MIN, "min")
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what == "check":
        run_check()
    elif what == "probe":
        run_news(probe=True)
    elif what == "sign":
        sync(); run_sign(); sync()
    elif what == "fetch":
        run_fetch(os.environ.get("FETCH_URLS", ""))
    elif what == "delete":
        run_delete(os.environ.get("MESSAGE_ID", "").strip())
    elif what == "videos":
        run_all(videos=True, news=False)
    elif what == "news":
        run_all(videos=False, news=True)
    else:
        run_all()
