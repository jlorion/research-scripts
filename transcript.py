import os
import glob
import json
import whisper

audio_folder = "audio_data_v2"
output_folder = "transcripts"
os.makedirs(output_folder, exist_ok=True)

model = whisper.load_model("medium")  # You can use "small", "medium", or "large" for better accuracy

audio_files = glob.glob(os.path.join(audio_folder, "*.mp3"))

for audio_path in audio_files:
    filename = os.path.splitext(os.path.basename(audio_path))[0]
    transcript_path = os.path.join(output_folder, f"{filename}.json")
    if os.path.exists(transcript_path):
        print(f"Transcript exists: {transcript_path}")
        continue
    print(f"Transcribing: {audio_path}")
    result = model.transcribe(audio=audio_path)
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Saved: {transcript_path}")