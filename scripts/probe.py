import re, urllib.request
UA = {"User-Agent": "Mozilla/5.0"}
for u in ["https://qalampir.uz/uz", "https://qalampir.uz/uz/news", "https://qalampir.uz/uz/latest", "https://qalampir.uz/sitemap.xml", "https://qalampir.uz/uz/sitemap.xml"]:
    try:
        raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode("utf-8", "ignore")
        links = re.findall(r'href="(/uz/news/[^"]+)"', raw)
        print("OK", u, len(raw), "news links:", len(links), links[:5])
        for m in re.finditer(r'<a[^>]+href="(/uz/news/[^"]+)"[^>]*>(.*?)</a>', raw, re.S):
            t = re.sub(r"<[^>]+>", " ", m.group(2)); t = re.sub(r"\s+", " ", t).strip()
            if t:
                print("  A", m.group(1)[:80], "|", t[:90])
                break
        print("  RSS hints:", re.findall(r'(application/rss\+xml[^>]*)', raw)[:3], re.findall(r'href="([^"]*rss[^"]*)"', raw)[:5])
        print("  time hints:", re.findall(r'(\d{2}:\d{2}[^<]{0,20})', raw)[:5])
        if "sitemap" in u:
            print("  sitemap sample:", raw[:600])
    except Exception as e:
        print("FAIL", u, e)
