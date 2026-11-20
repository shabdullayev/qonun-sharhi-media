"""Rasm yaratish (GitHub Actions): img/in/<kalit>.json -> img/out/<kalit>/<nom>.png (Gemini «Nano Banana»).

Kirish fayli:
{
  "model": "gemini-3.1-flash-image",          # ixtiyoriy
  "images": [
    {"name": "sahna01", "prompt": "...", "aspect": "9:16", "size": "2K",
     "refs": ["img/out/cast/yigit_oddiy.png"]}   # ixtiyoriy: bir xil qahramon uchun namuna rasmlar
  ]
}
Har bir promptning boshiga img/style.txt dagi umumiy uslub qo‘shiladi.
"""
import glob, json, os, sys, time

from google import genai
from google.genai import types

DEFAULT_MODEL = os.environ.get("IMG_MODEL", "gemini-3.1-flash-image")
STYLE = open("img/style.txt", encoding="utf-8").read().strip() if os.path.exists("img/style.txt") else ""


def gen(client, model, item, path):
    parts = []
    for r in item.get("refs", []):
        parts.append(types.Part.from_bytes(data=open(r, "rb").read(), mime_type="image/png"))
    parts.append(types.Part.from_text(text=(STYLE + "\n\n" + item["prompt"]).strip()))
    cfg = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio=item.get("aspect", "9:16"), image_size=item.get("size", "2K")),
    )
    for attempt in range(4):
        try:
            resp = client.models.generate_content(model=model, contents=parts, config=cfg)
            for c in resp.candidates or []:
                for p in c.content.parts or []:
                    if p.inline_data and p.inline_data.data:
                        open(path, "wb").write(p.inline_data.data)
                        return
            print("rasm qaytmadi, qayta urinish:", item["name"])
        except Exception as e:
            print("xato, qayta urinish:", item["name"], e)
        time.sleep(10 * (attempt + 1))
    raise SystemExit("rasm yaratilmadi: " + path)


def main():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("::warning::GEMINI_API_KEY secret topilmadi (Settings → Secrets and variables → Actions). Rasm yaratilmadi.")
        return
    client = genai.Client(api_key=key)
    only = sys.argv[1:]
    for f in sorted(glob.glob("img/in/*.json")):
        k = os.path.splitext(os.path.basename(f))[0]
        if only and k not in only:
            continue
        d = json.load(open(f, encoding="utf-8"))
        d["_style"] = STYLE
        out = f"img/out/{k}"
        done = out + "/done.json"
        if os.path.exists(done) and json.load(open(done, encoding="utf-8")) == d:
            continue
        os.makedirs(out, exist_ok=True)
        for item in d["images"]:
            gen(client, d.get("model", DEFAULT_MODEL), item, f"{out}/{item['name']}.png")
            print("tayyor", k, item["name"])
        json.dump(d, open(done, "w", encoding="utf-8"), ensure_ascii=False)


main()
