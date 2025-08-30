from fastapi import FastAPI
from PIL import ImageGrab
import uvicorn
import io

app = FastAPI()


def screenshot_desktop(file_path: str = "screenshot.png") -> None:
    img = ImageGrab.grab()
    img.save(file_path, format="PNG")
    print("Screenshot saved")


@app.get("/screenshot")
async def screenshot():
    screenshot_desktop()

    return {"done": True}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
