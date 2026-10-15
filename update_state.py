import json
from pathlib import Path
import sys

sys.path.insert(0, "/root/YT_vaibhavsisinty")
from git_manager import update_readme_index, commit_and_push_repo

state_file = Path("/root/YT_vaibhavsisinty/state.json")
cat_file = Path("/root/YT_vaibhavsisinty/catalog.json")
cat = json.load(open(cat_file, encoding="utf-8"))

res = {
    "id": "2XpIMa1BSPc",
    "title": "Google Gemini 4 Argon Is Here. We Tested It (+11 AI Updates)",
    "title_fr": "Google Gemini 4 Argon est arrivé. Nous l'avons testé (+11 nouveautés IA)",
    "upload_date": "20261015",
    "duration": 1242,
    "duration_str": "00:20:42",
    "md_file": "YT_vaibhavsisinty_Transcript/2026-10-15_YT-[2XpIMa1BSPc]_Google Gemini 4 Argon est arrivé. Nous l'avons testé (+11 nouveautés IA)_by-[whisper-v3-large-turbo+gemini-3.5-flash-lite].md",
    "html_file": "YT_vaibhavsisinty_Transcript/2026-10-15_YT-[2XpIMa1BSPc]_Google Gemini 4 Argon est arrivé. Nous l'avons testé (+11 nouveautés IA)_by-[whisper-v3-large-turbo+gemini-3.5-flash-lite].html",
    "screenshots_count": 81,
    "audit_score": 100.0,
    "audit_passed": True
}

state = {
    "processed_ids": ["2XpIMa1BSPc"],
    "processed_videos": [res],
    "completed_count": 1,
    "total_catalog": len(cat),
    "known_baseline_ids": [v["id"] for v in cat if "id" in v]
}
with open(state_file, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

update_readme_index(state["processed_videos"], total_catalog_count=len(cat))
commit_and_push_repo("feat: transcription 2XpIMa1BSPc - Google Gemini 4 Argon est arrivé")
print("SUCCESS: State updated and pushed to GitHub!")
