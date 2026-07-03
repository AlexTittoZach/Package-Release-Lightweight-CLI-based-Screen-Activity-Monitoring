from pathlib import Path
import os

APP_DIR = (
    Path(os.getenv("LOCALAPPDATA"))
    / "ScreenTracker"
)

APP_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DB_PATH = APP_DIR / "usage.db"