import subprocess
import os
import sys

def start_recording(output_filename, audio_device="CABLE Output (VB-Audio Virtual Cable)"):
    """
    Starts recording audio from a specified dshow audio device using ffmpeg.

    This function runs ffmpeg as a background process.

    Args:
        output_filename (str): The path for the output audio file (e.g., 'meeting.m4a').
        audio_device (str): The name of the audio device to record from.

    Returns:
        subprocess.Popen: The process object for the running ffmpeg command.
                         Returns None if ffmpeg command fails to start or file exists.
    """
    if os.path.exists(output_filename):
        print(f"Error: Output file '{output_filename}' already exists. Please remove it or choose a different name.")
        return None

    command = [
        'ffmpeg',
        '-f', 'dshow',
        '-i', f'audio={audio_device}',
        '-c:a', 'aac',
        '-b:a', '64k',
        output_filename
    ]

    print(f"Starting recording from '{audio_device}'...")
    print(f"Command: {' '.join(command)}")

    try:
        # Use Popen to run ffmpeg in the background.
        # stdin=subprocess.PIPE allows us to send commands (like 'q') to ffmpeg.
        creationflags = 0
        if sys.platform == "win32":
            # This flag prevents the ffmpeg console window from appearing.
            creationflags = subprocess.CREATE_NO_WINDOW

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=creationflags, text=True, encoding='utf-8')
        return process
    except FileNotFoundError:
        print("Error: 'ffmpeg' not found. Please ensure ffmpeg is installed and in your system's PATH.")
        return None
    except Exception as e:
        print(f"An error occurred while starting ffmpeg: {e}")
        return None

def stop_recording(process):
    """
    Stops an ffmpeg recording process gracefully by sending 'q'.

    Args:
        process (subprocess.Popen): The ffmpeg process to stop.

    Returns:
        bool: True if the process was stopped, False if it was not running.
    """
    if not process or process.poll() is not None: # Check if the process is not running or has already finished
        return False

    print("Stopping recording...")
    try:
        # Sending 'q' to ffmpeg's stdin is the graceful way to stop recording.
        process.communicate(input='q', timeout=10)
        print("Recording stopped gracefully.")
    except subprocess.TimeoutExpired:
        print("ffmpeg did not respond to 'q' within 10 seconds, terminating process.")
        process.kill()
        process.communicate()
    return True

if __name__ == '__main__':
    output_file = "meeting_recording.m4a"
    recording_process = start_recording(output_file)

    if recording_process:
        print("Recording is in progress. Press Enter to stop.")
        try:
            input() # Wait for user to press Enter
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
        finally:
            stop_recording(recording_process)
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                print(f"Recording saved to {output_file}")
            else:
                print("Recording failed or was cancelled before data was written.")