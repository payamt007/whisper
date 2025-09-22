import os
import time
import glob

import whisper


def transcribe():
    try:
        start = time.time()
        print("Loading Whisper model...")
        model = whisper.load_model("small", device="cuda")

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(ROOT_DIR, "voice_capture")
        audio_files = glob.glob(os.path.join(audio_dir, "*.m4a"))
        if not audio_files:
            raise FileNotFoundError(f"No .mkv files found in {audio_dir}")
        audio_file = max(audio_files, key=os.path.getctime)
        # audio_file = os.path.join(ROOT_DIR, "voice_capture", "2025-09-12 11-55-56.mkv")
        # Check if audio file exists
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file {audio_file} not found")

        print("Processing audio...")
        result = model.transcribe(audio_file)

        print(result["text"])

        end = time.time()

        print("Time taken: {:.2f} seconds".format(end - start))

        return result["text"]

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    transcribe()
