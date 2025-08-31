from fastapi import FastAPI, HTTPException
from PIL import ImageGrab
import uvicorn
import datetime
import os
import json
import psutil
from record import start_recording, stop_recording

app = FastAPI()

# --- State Management ---

STATE_FILE = ".recording_state.json"

# Global state to hold the recording process and filename
# NOTE: This simple global variable works for a single-process server.
# For multi-worker setups, a more robust state management (e.g., Redis, file lock) is needed.
recording_state = {
    "process": None,
    "filename": None
}

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

# --- Endpoints ---

def screenshot_desktop(file_path: str = "screenshot.png") -> None:
    img = ImageGrab.grab()
    img.save(file_path, format="PNG")
    print("Screenshot saved")


@app.get("/screenshot")
async def screenshot():
    screenshot_desktop()

    return {"done": True}

@app.post("/start-recording")
async def start_rec_endpoint():
    if recording_state["process"] is not None and recording_state["process"].poll() is None:
        raise HTTPException(status_code=400, detail=f"Recording is already in progress. Output file: {recording_state['filename']}")

    # Generate a unique filename to avoid overwrites
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"recording_{timestamp}.m4a"

    process = start_recording(output_filename)

    if process is None:
        # The start_recording function prints errors, but we raise an HTTP exception for the client.
        raise HTTPException(status_code=500, detail="Failed to start recording. Check server logs for details.")

    # Persist state to file and memory
    _save_state_to_file(process.pid, output_filename)
    recording_state["process"] = process
    recording_state["filename"] = output_filename

    return {"message": "Recording started", "output_file": output_filename}

@app.post("/stop-recording")
async def stop_rec_endpoint():
    process = recording_state["process"]
    filename = recording_state["filename"]

    if not stop_recording(process):
        raise HTTPException(status_code=400, detail="No active recording found to stop.")

    _clear_state_file()
    # Reset the state
    recording_state["process"] = None
    recording_state["filename"] = None

    return {"message": "Recording stopped successfully", "output_file": filename}



@app.get("/decode")
async def decode():
    ...

if __name__ == "__main__":
    # Run validation on startup before starting the server
    _load_and_validate_state()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
