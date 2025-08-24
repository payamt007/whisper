import os
from faster_whisper import WhisperModel

# Add ffmpeg to PATH
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-n7.1-latest-win64-lgpl-7.1\ffmpeg-n7.1-latest-win64-lgpl-7.1\bin"

try:
    print("Loading Whisper model...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")

    # Check if audio file exists
    audio_file = "my_recording1.wav"
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file {audio_file} not found")

    print("Processing audio...")
    segments, info = model.transcribe(audio_file)

    print(f"Detected language: {info.language}")
    print("Transcription:")

    for segment in segments:
        print(segment.text)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()