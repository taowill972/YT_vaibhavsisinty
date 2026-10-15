import json
import subprocess
import sys
from pathlib import Path
from config import CATALOG_FILE, CHANNEL_ID, PROXY, PLAYER_CLIENT

def dump_catalog():
    print(f"[Catalog] Extraction du catalogue complet pour le canal {CHANNEL_ID}...", flush=True)
    cmd = [
        "yt-dlp",
        "--proxy", PROXY,
        "--extractor-args", f"youtube:player_client={PLAYER_CLIENT}",
        "--flat-playlist",
        "--dump-json",
        f"https://www.youtube.com/channel/{CHANNEL_ID}/videos"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    entries = []
    seen = set()
    for line in res.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            vid_id = d.get("id")
            if vid_id and vid_id not in seen:
                seen.add(vid_id)
                entries.append({
                    "id": vid_id,
                    "title": d.get("title", ""),
                    "upload_date": d.get("upload_date") or "",
                    "duration": d.get("duration"),
                    "duration_string": d.get("duration_string", ""),
                    "webpage_url": f"https://www.youtube.com/watch?v={vid_id}"
                })
        except Exception:
            pass

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"[Catalog] ✅ Extraction terminée : {len(entries)} vidéos sauvegardées dans {CATALOG_FILE}", flush=True)
    return entries

if __name__ == "__main__":
    dump_catalog()
