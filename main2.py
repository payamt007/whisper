import os
import whisper

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-n7.1-latest-win64-lgpl-7.1\ffmpeg-n7.1-latest-win64-lgpl-7.1\bin"

try:
    model = whisper.load_model("tiny")
    audio = whisper.load_audio("my_recording1.wav")
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    print(result.text)
except Exception as e:
    print(f"Error: {e}")