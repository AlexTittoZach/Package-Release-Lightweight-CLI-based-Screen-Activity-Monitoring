from pathlib import Path
import os
import atexit
import psutil

APP_DIR = (
    Path.home()
    / "AppData"
    / "Local"
    / "ScreenTracker"
)

APP_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOCK_FILE = APP_DIR / "tracker.lock"


def acquire_lock():

    if LOCK_FILE.exists():

        try:

            pid = int(
                LOCK_FILE.read_text()
            )

            if psutil.pid_exists(pid):

                return False

            LOCK_FILE.unlink()

        except Exception:

            LOCK_FILE.unlink()

    LOCK_FILE.write_text(
        str(os.getpid())
    )

    atexit.register(
        release_lock
    )

    return True


def release_lock():

    if LOCK_FILE.exists():

        LOCK_FILE.unlink()