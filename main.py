import whisper

model: whisper.Whisper = whisper.load_model("base")

result = model.transcribe(audio="./my_recording1.wav",verbose=True, fp16=False)

print("\n--- Full Transcription Result ---")
print(result)