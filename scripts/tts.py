"""Ovoz yaratish (GitHub Actions): tts/in/<kalit>.json -> tts/out/<kalit>/NN.mp3 (edge-tts, o‘zbek neyron ovozi)."""
import asyncio, glob, json, os

import edge_tts

# Ovoz tezligi: 2026-11-16 dan boshlab yangi videolarda ovoz biroz tezroq.
# Har bir tts/in/<kalit>.json da "rate" berilsa o‘sha ishlatiladi, aks holda shu standart.
DEFAULT_RATE = "+15%"


async def one(text, voice, path, rate=DEFAULT_RATE):
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(path)
            if os.path.getsize(path) > 1000:
                return
        except Exception as e:  # tarmoq xatosi — qayta urinish
            print("qayta urinish", path, e)
            await asyncio.sleep(3 * (attempt + 1))
    raise SystemExit("ovoz yaratilmadi: " + path)


async def main():
    for f in sorted(glob.glob("tts/in/*.json")):
        key = os.path.splitext(os.path.basename(f))[0]
        d = json.load(open(f, encoding="utf-8"))
        out = f"tts/out/{key}"
        if os.path.exists(out + "/done.json") and json.load(open(out + "/done.json", encoding="utf-8")) == d:
            continue
        os.makedirs(out, exist_ok=True)
        for i, t in enumerate(d["segments"]):
            await one(t, d["voice"], f"{out}/{i:02d}.mp3", d.get("rate", DEFAULT_RATE))
        json.dump(d, open(out + "/done.json", "w", encoding="utf-8"), ensure_ascii=False)
        print("tayyor", key, len(d["segments"]))


asyncio.run(main())
