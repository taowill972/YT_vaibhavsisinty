import os
from pathlib import Path

# Paths VPS
BASE_DIR = Path("/root/YT_vaibhavsisinty")
REPO_DIR = BASE_DIR
TRANSCRIPTS_DIR = BASE_DIR / "YT_vaibhavsisinty_Transcript"
CATALOG_FILE = BASE_DIR / "catalog.json"
STATE_FILE = BASE_DIR / "state.json"
WORK_DIR = Path("/tmp/yt_vaibhavsisinty_work")
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
LOG_FILE = Path("/var/log/yt_vaibhavsisinty.log")

# Channel Information
CHANNEL_ID = "UClXAalunTPaX1YV185DWUeg"
CHANNEL_NAME = "Vaibhav Sisinty"
CHANNEL_HANDLE = "@vaibhavsisinty"
CHANNEL_URL = "https://www.youtube.com/@vaibhavsisinty"
RSS_FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
CHANNEL_DOMAIN = "AI Tools, Growth Hacking, Automatisation, IA Générative, Marketing Digital, Prompt Engineering, Agents IA, Productivité"

# Models
AUDIO_GEMINI_MODEL = "gemini-3.5-flash-lite"
AUDIO_FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-3.8-flash"]
WHISPER_MODEL = "large-v3-turbo"

VISUAL_GEMINI_MODEL = "gemini-3.5-flash-lite"
VISUAL_FALLBACK_MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash"]

MODEL_SIGNATURE = f"whisper-v3-large-turbo+{VISUAL_GEMINI_MODEL}"

# API Keys & Network
AUDIO_KEYS_FILE = BASE_DIR / "gemini_audio_keys.txt"
VISUAL_KEYS_FILE = BASE_DIR / "gemini_visual_keys.txt"
PROXY = "socks5://127.0.0.1:4001"
PLAYER_CLIENT = "android"

# Processing parameters
BATCH_SIZE = 7
MAX_BLOCK_DURATION = 32.0
MIN_BLOCK_DURATION = 18.0
FRAME_DIFF_THRESHOLD = 15.0
FRAME_MAX_WIDTH = 1280

# Ensure directories exist
BASE_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)
