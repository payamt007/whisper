import json
import os

import psutil
from PIL import ImageGrab

STATE_FILE="process-config.json"


def _load_and_validate_state():
    """Checks for a state file on startup to handle crash recovery."""
    if os.path.exists(STATE_FILE):
        print(f"INFO: Found existing state file '{STATE_FILE}', indicating a previous crash. Validating...")
        with open(STATE_FILE, 'r') as f:
            try:
                state = json.load(f)
            except json.JSONDecodeError:
                print("ERROR: State file is corrupt. Cleaning up.")
                _clear_state_file()
                return

        pid = state.get("pid")
        filename = state.get("filename")

        if pid and psutil.pid_exists(pid):
            try:
                p = psutil.Process(pid)
                # For safety, check if the process name is ffmpeg
                if 'ffmpeg' in p.name().lower():
                    print(f"INFO: Orphaned recording process {pid} found. Terminating it.")
                    p.kill() # Kill the zombie process
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process is already gone or we can't access it, which is fine.
                print(f"INFO: Process {pid} already gone or inaccessible.")

        if filename and os.path.exists(filename):
            print(f"INFO: Cleaning up potentially corrupt recording file: {filename}")
            os.remove(filename)

        _clear_state_file()
        print("INFO: State cleanup complete. Server is in a clean state.")


def _save_state_to_file(pid, filename):
    with open(STATE_FILE, 'w') as f:
        json.dump({"pid": pid, "filename": filename}, f)


def _clear_state_file():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)


def screenshot_desktop(file_path: str = "screenshot.png") -> None:
    img = ImageGrab.grab()
    img.save(file_path, format="PNG")
    print("Screenshot saved")
