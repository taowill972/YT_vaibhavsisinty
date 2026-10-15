import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, List

from config import (
    BASE_DIR,
    REPO_DIR,
    CATALOG_FILE,
    STATE_FILE,
    BATCH_SIZE
)
from pipeline import process_single_video
from git_manager import update_readme_index, commit_and_push_repo

def disable_cron_batch_job() -> bool:
    try:
        res = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        lines = res.stdout.splitlines()
        new_lines = [l for l in lines if "YT_vaibhavsisinty/run_cron.sh" not in l and "yt_vaibhavsisinty" not in l]
        if len(new_lines) != len(lines):
            new_cron = "\n".join(new_lines) + "\n"
            p = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
            p.communicate(new_cron)
            print("[BatchRunner] 🛑 Crontab 6h retiré avec succès : routine désactivée suite à la complétion intégrale.", flush=True)
            return True
        return False
    except Exception as e:
        print(f"[BatchRunner] Erreur lors de la désactivation du cron : {e}", flush=True)
        return False

def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "processed_ids": [],
        "processed_videos": [],
        "last_run_timestamp": None,
        "completed_count": 0,
        "total_catalog": 0
    }

def save_state(state: Dict[str, Any]) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def main():
    print(f"\n====================================================================", flush=True)
    print(f"🚀 [BatchRunner] Démarrage de la routine (Lot de {BATCH_SIZE} vidéos)", flush=True)
    print(f"⏱️ Horodatage : {time.strftime('%Y-%m-%d %H:%M:%S UTC')}", flush=True)
    print(f"====================================================================", flush=True)

    if not CATALOG_FILE.exists():
        print(f"[BatchRunner] Catalogue absent, extraction initiale...", flush=True)
        from dump_catalog import dump_catalog
        catalog = dump_catalog()
    else:
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            catalog = json.load(f)

    # Le catalogue extrait depuis la section /videos est naturellement ordonné du plus récent au plus ancien
    unprocessed = [v for v in catalog if v.get("id") and v.get("id") not in processed_ids]
    print(f"[BatchRunner] Progression globale : {len(processed_ids)} / {len(catalog)} traitées ({len(unprocessed)} restantes).", flush=True)

    if not unprocessed:
        print("[BatchRunner] 🎉 TOUTES LES VIDÉOS DU CATALOGUE ONT ÉTÉ ENTIÈREMENT TRAITÉES !", flush=True)
        disable_cron_batch_job()
        print("[BatchRunner] Seul le démon d'écoute passif reste actif.", flush=True)
        return

    # Sélection du lot de BATCH_SIZE vidéos
    batch = unprocessed[:BATCH_SIZE]
    print(f"[BatchRunner] 🎯 Traitement du lot de {len(batch)} vidéos : {[v['id'] for v in batch]}", flush=True)

    for i, v in enumerate(batch):
        vid_id = v["id"]
        v_title = v.get("title", "")
        print(f"\n[{i+1}/{len(batch)}] Lancement : {vid_id} — {v_title}", flush=True)

        try:
            res = process_single_video(vid_id, catalog_title=v_title, use_gemini_audio=False)
            state["processed_ids"].append(vid_id)
            state["processed_videos"].append(res)
            state["completed_count"] = len(state["processed_ids"])
            state["last_run_timestamp"] = time.time()
            save_state(state)

            update_readme_index(state["processed_videos"], total_catalog_count=len(catalog))
            commit_and_push_repo(f"feat: transcription {vid_id} - {res.get('title_fr', v_title)[:50]}")
            print(f"[BatchRunner] ✓ Vidéo {vid_id} traitée, indexée et poussée sur GitHub avec succès.", flush=True)

        except Exception as e:
            print(f"[BatchRunner] ❌ Échec sur la vidéo {vid_id} : {e}", flush=True)

    # Vérification post-lot : reste-t-il des vidéos ?
    remaining_after_batch = len(catalog) - len(state["processed_ids"])
    if remaining_after_batch <= 0:
        print("\n[BatchRunner] 🏁 Toutes les vidéos du catalogue sont désormais traitées !", flush=True)
        disable_cron_batch_job()

if __name__ == "__main__":
    main()
