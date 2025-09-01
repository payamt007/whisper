import json
import os
import glob
from typing import List
from src.types import RecordingInfo
import datetime

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


def list_files(file_pattern:str="recording_*.m4a") -> List[RecordingInfo]:
    """
    Retrieves a list of all saved recordings, sorted by most recent first.
    """
    recording_files = glob.glob(os.path.join("src","assets", file_pattern))

    response_data = []
    for file_path in recording_files:
        try:
            file_size = os.path.getsize(file_path)
            mod_time = os.path.getctime(file_path)
            response_data.append(
                RecordingInfo(
                    filename=file_path,
                    size_bytes=file_size,
                    creation_time=datetime.datetime.fromtimestamp(mod_time).isoformat(),
                )
            )
        except FileNotFoundError:
            # In the unlikely event a file is deleted between glob and getsize
            continue

    # Sort by modification time, newest first
    response_data.sort(key=lambda r: r.creation_time, reverse=True)

    return response_data