from fastapi import FastAPI
import uvicorn

from typing import List

from src.helpers import _load_and_validate_state, screenshot_desktop, list_files
from src.defined_types import RecordingInfo
from src.old_recorder.router import router as legacy_recorder_router

app = FastAPI()

app.include_router(legacy_recorder_router)


@app.get("/screenshot")
async def screenshot():
    screenshot_desktop()

    return {"done": True}


@app.get("/list-files", response_model=List[RecordingInfo])
async def list_recordings(file_type: str = None):
    if file_type == "recording":
        return list_files("*.m4a")
    elif file_type == "screenshot":
        return list_files("*.jpg")
    else:
        return []

    return list_files()


if __name__ == "__main__":
    # Run validation on startup before starting the server
    _load_and_validate_state()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
