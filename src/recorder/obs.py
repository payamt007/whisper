import sys
from obswebsocket import obsws, requests, exceptions

### --- Connection Settings ---
HOST = "localhost"
PORT = 4455
# Use the password you got from OBS "Show Connect Info"
PASSWORD = "w0D4VioKrOmDZr0a"

def main():
    """Connects to OBS and sends a start/stop recording command."""
    # Check if a command was passed (e.g., "start" or "stop")
    if len(sys.argv) < 2 or sys.argv[1] not in ["start", "stop"]:
        print(f"Usage: python {sys.argv[0]} <start|stop>")
        sys.exit(1)

    command = sys.argv[1]
    ws = obsws(HOST, PORT, PASSWORD)
    is_connected = False

    try:
        # Connect to OBS
        ws.connect()
        print("Successfully connected to OBS WebSocket.")
        is_connected = True

        if command == "start":
            print("Sending request to start recording...")
            ws.call(requests.StartRecord())
            print("Recording started.")

        elif command == "stop":
            print("Sending request to stop recording...")
            response = ws.call(requests.StopRecord())
            # The obswebsocket library returns an object with a getData() method
            output_path = response.get_data().get('outputPath')
            print(f"Recording stopped. File saved to: {output_path}")

    except exceptions.ConnectionFailure:
        print("Error: Could not connect to OBS WebSocket. Is OBS running and is the WebSocket Server enabled?")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        # Ensure we disconnect if a connection was successfully established
        if is_connected:
            ws.disconnect()
            print("Disconnected from OBS WebSocket.")

if __name__ == "__main__":
    main()
