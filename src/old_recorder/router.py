from fastapi import APIRouter
from fastapi import HTTPException
import datetime
from src.record import start_recording, stop_recording
from src.helpers import _save_state_to_file, _clear_state_file

router = APIRouter()

recording_state = {
    "process": None,
    "filename": None
}


@router.post("/start-recording")
async def start_rec_endpoint():
    if recording_state["process"] is not None and recording_state["process"].poll() is None:
        raise HTTPException(status_code=400,
                            detail=f"Recording is already in progress. Output file: {recording_state['filename']}")

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


@router.post("/stop-recording")
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
