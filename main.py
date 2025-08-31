from fastapi import FastAPI, HTTPException
from PIL import ImageGrab
import uvicorn
import datetime
from record import start_recording, stop_recording

app = FastAPI()

# Global state to hold the recording process and filename
# NOTE: This simple global variable works for a single-process server.
# For multi-worker setups, a more robust state management (e.g., Redis, file lock) is needed.
recording_state = {
    "process": None,
    "filename": None
}

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

    recording_state["process"] = process
    recording_state["filename"] = output_filename

    return {"message": "Recording started", "output_file": output_filename}

@app.post("/stop-recording")
async def stop_rec_endpoint():
    process = recording_state["process"]
    filename = recording_state["filename"]

    if not stop_recording(process):
        raise HTTPException(status_code=400, detail="No active recording found to stop.")

    # Reset the state
    recording_state["process"] = None
    recording_state["filename"] = None

    return {"message": "Recording stopped successfully", "output_file": filename}

@app.get("/decode")
async def decode():
    ...

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
