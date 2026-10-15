import subprocess
from pathlib import Path
from typing import List, Dict, Any

from config import (
    REPO_DIR,
    TRANSCRIPTS_DIR,
    CHANNEL_NAME,
    CHANNEL_URL,
    CHANNEL_HANDLE,
    MODEL_SIGNATURE
)

def update_readme_index(processed_videos: List[Dict[str, Any]], total_catalog_count: int = 0) -> None:
    readme_path = REPO_DIR / "README.md"
    pct = (len(processed_videos) / total_catalog_count * 100) if total_catalog_count > 0 else 0

    lines = [
        f"# 🎬 YT_vaibhavsisinty — Veille & Transcriptions Multimodales",
        "",
        f"> Base de connaissances et transcriptions intégrales mot pour mot en français (audio via `Whisper-v3-large-turbo`) et descriptions visuelles d'écran (via `gemini-3.5-flash-lite`) avec captures d'écran clés et fiches interactives HTML de la chaîne **[{CHANNEL_NAME}]({CHANNEL_URL})** ({CHANNEL_HANDLE}).",
        "",
        "## 📁 Organisation des Fichiers",
        "- Tous les rapports `.md` et pages interactives `.html` sont centralisés dans le dossier dédié : **`YT_vaibhavsisinty_Transcript/`**",
        "- Les captures d'écran par timeline sont archivées dans : **`screenshots/<video_id>/`**",
        "",
        "## 📊 Statistiques de l'Automatisation",
        f"- **Vidéos traitées** : `{len(processed_videos)} / {total_catalog_count}` (`{pct:.1f}%`)",
        f"- **Modèle Audio & Synthèse** : `Whisper-v3-large-turbo` (100% Verbatim Français)",
        f"- **Modèle Vision d'écran** : `gemini-3.5-flash-lite` (Analyse d'écrans, outils IA, SaaS, prompts & démonstrations)",
        f"- **Signature de traitement** : `{MODEL_SIGNATURE}`",
        f"- **Mode Opératoire** : Zéro coquille vide (Mode X - Sincérité Technique Absolue)",
        "",
        "## 📑 Index Exhaustif des Vidéos Analysées",
        "",
        "| Date | Réf. Vidéo | Titre Français / Sujet | Fiche Markdown | Fiche Interactive HTML | Captures |",
        "| :--- | :--- | :--- | :--- | :--- | :---: |"
    ]

    for item in sorted(processed_videos, key=lambda x: x.get("upload_date", ""), reverse=True):
        date_str = item.get("upload_date", "N/A")
        if len(date_str) == 8:
            date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        else:
            date_formatted = date_str

        vid_id = item.get("id", "")
        title_fr = item.get("title_fr", item.get("title", ""))
        md_file = item.get("md_file", "")
        html_file = item.get("html_file", "")
        n_screens = item.get("screenshots_count", 0)

        yt_link = f"[{vid_id}](https://www.youtube.com/watch?v={vid_id})"
        md_link = f"[{Path(md_file).name}]({md_file})" if md_file else "-"
        html_link = f"[Voir Rapport HTML]({html_file})" if html_file else "-"

        lines.append(f"| {date_formatted} | {yt_link} | **{title_fr}** | {md_link} | {html_link} | `{n_screens}` |")

    lines.append("")
    lines.append("---")
    lines.append("*Généré automatiquement par l'agent de veille multimodale Antigravity sur VPS Contabo.*")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[GitManager] README.md mis à jour ({len(processed_videos)} vidéos indexées).", flush=True)

def commit_and_push_repo(commit_msg: str) -> bool:
    try:
        subprocess.run(["git", "add", "."], cwd=REPO_DIR, check=True, capture_output=True)

        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_DIR, capture_output=True, text=True, check=True
        )
        if not status_res.stdout.strip():
            print("[GitManager] Aucun nouveau changement à commiter.", flush=True)
            return True

        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=REPO_DIR, check=True, capture_output=True
        )
        print(f"[GitManager] Commit créé : '{commit_msg}'", flush=True)

        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=REPO_DIR, check=True, capture_output=True
        )
        print(f"[GitManager] 🚀 Déploiement GitHub réussi vers origin/main.", flush=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[GitManager] Erreur Git (code {e.returncode}) : {e.stderr}", flush=True)
        return False
    except Exception as e:
        print(f"[GitManager] Erreur commit/push : {e}", flush=True)
        return False
