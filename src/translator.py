import os
import time
import glob

from faster_whisper import WhisperModel


# Add ffmpeg to PATH
# os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-n7.1-latest-win64-lgpl-7.1\ffmpeg-n7.1-latest-win64-lgpl-7.1\bin"

def transcribe():
    try:
        start = time.time()
        print("Loading Whisper model...")
        model = WhisperModel("tiny", device="cpu", compute_type="int8")

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(ROOT_DIR, "voice_capture")
        audio_files = glob.glob(os.path.join(audio_dir, "*.mkv"))
        if not audio_files:
            raise FileNotFoundError(f"No .mkv files found in {audio_dir}")
        audio_file = max(audio_files, key=os.path.getctime)
        # audio_file = os.path.join(ROOT_DIR, "voice_capture", "2025-09-12 11-55-56.mkv")
        # Check if audio file exists
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file {audio_file} not found")

        print("Processing audio...")
        # To further increase speed, you can adjust transcription parameters:
        # - beam_size=1: Uses greedy decoding, which is faster but potentially less accurate.
        # - vad_filter=True: Skips silent parts of the audio, which can significantly
        #   speed up transcription for audio with pauses.
        # segments, info = model.transcribe(audio_file, beam_size=1, vad_filter=True)
        segments, info = model.transcribe(audio_file)

        print(f"Detected language: {info.language}")
        print("Transcription:")

        output = ""

        for segment in segments:
            output += segment.text
            print(segment.text)

        end = time.time()

        print("Time taken: {:.2f} seconds".format(end - start))

        return output

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    transcribe()
