from fastapi import FastAPI, HTTPException
import uvicorn
import datetime
import os
from src.record import start_recording, stop_recording
import glob
from typing import List

from src.helpers import _load_and_validate_state, _save_state_to_file, _clear_state_file, screenshot_desktop
from src.types import RecordingInfo

app = FastAPI()

recording_state = {
    "process": None,
    "filename": None
}

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

@app.get("/recordings", response_model=List[RecordingInfo])
async def list_recordings():
    """
    Retrieves a list of all saved recordings, sorted by most recent first.
    """
    file_pattern = "recording_*.m4a"
    recording_files = glob.glob(file_pattern)

    response_data = []
    for file_path in recording_files:
        try:
            file_size = os.path.getsize(file_path)
            mod_time = os.path.getmtime(file_path)
            response_data.append(
                RecordingInfo(
                    filename=file_path,
                    size_bytes=file_size,
                    modified_time=datetime.datetime.fromtimestamp(mod_time).isoformat(),
                )
            )
        except FileNotFoundError:
            # In the unlikely event a file is deleted between glob and getsize
            continue

    # Sort by modification time, newest first
    response_data.sort(key=lambda r: r.modified_time, reverse=True)

    return response_data

if __name__ == "__main__":
    # Run validation on startup before starting the server
    _load_and_validate_state()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
