from fastapi import APIRouter
from obswebsocket import obsws, requests, exceptions

### --- Connection Settings ---
HOST = "localhost"
PORT = 4455
PASSWORD = "w0D4VioKrOmDZr0a"
ws = obsws(HOST, PORT, PASSWORD)
router = APIRouter()


@router.post("/start-record")
async def start_obs_recording():
    is_connected = False
    try:
        # Connect to OBS
        ws.connect()
        print("Successfully connected to OBS WebSocket.")
        is_connected = True

        print("Sending request to start recording...")
        ws.call(requests.StartRecord())
        print("Recording started.")

        return {"message": "Recording started"}

    except exceptions.ConnectionFailure:
        print("Error: Could not connect to OBS WebSocket. Is OBS running and is the WebSocket Server enabled?")
        return {"message": "Error Recording Start For Connection fails"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"message": "UnknowN Error"}
    finally:
        # Ensure we disconnect if a connection was successfully established
        if is_connected:
            ws.disconnect()
            print("Disconnected from OBS WebSocket.")


@router.post("/stop-record")
async def stop_obs_recording():
    is_connected = False
    try:
        # Connect to OBS
        ws.connect()
        print("Successfully connected to OBS WebSocket.")
        is_connected = True

        print("Sending request to stop recording...")
        response = ws.call(requests.StopRecord())
        # The obswebsocket library returns an object with a getData() method
        output_path = response.get_data().get('outputPath')
        print(f"Recording stopped. File saved to: {output_path}")

        return {"message": "Recording started"}

    except exceptions.ConnectionFailure:
        print("Error: Could not connect to OBS WebSocket. Is OBS running and is the WebSocket Server enabled?")
        return {"message": "Error Recording Start For Connection fails"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"message": "UnknowN Error"}
    finally:
        # Ensure we disconnect if a connection was successfully established
        if is_connected:
            ws.disconnect()
            print("Disconnected from OBS WebSocket.")
