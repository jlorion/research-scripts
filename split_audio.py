from pydub import AudioSegment
import pandas as pd
import os
import ulid
import json


audio_folder = "audio_data_v2"
output_audio_folder = "audio_data_v3"
transciprts_folder = "transcripts"
batch_csv_folder = "batch_csv"

# os.makedirs(output_folder, exist_ok=True)
arr_list = [
    os.path.splitext(f)[0] for f in os.listdir(transciprts_folder) if os.path.isfile(os.path.join(transciprts_folder, f))
]
print(len(arr_list))
csv_list = [
    os.path.splitext(f)[0] for f in os.listdir(batch_csv_folder) if os.path.isfile(os.path.join(batch_csv_folder, f))
]
print(len(csv_list))

df = pd.DataFrame(columns=["ulid", "text"])
index = 0
for item in arr_list: 
    index += 1
    if item not in csv_list:
        audio_path = os.path.join(audio_folder, f"{item}.mp3")
        if not os.path.exists(audio_path):
            print(f"Audio file does not exist: {audio_path}")
            continue
        audio_transcript = os.path.join(transciprts_folder, f"{item}.json")
        print(audio_path)
        print(audio_transcript)
        with open(audio_transcript, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        # do splitting here
        if transcript["text"] != "" and transcript["language"] in ("en", "tl", "es"):
            transcript_df = pd.DataFrame(columns=["ulid", "text"])
            segments = transcript["segments"]
            for segment in segments:
                if segment["text"].strip() == "" or (segment["end"] - segment["start"]) <= 1.0 or segment["text"].strip() in df["text"].values or segment["text"].strip() in transcript_df["text"].values:
                    continue
                ulid_str = str(ulid.ULID())
                new_audio = AudioSegment.from_file(audio_path)
                new_audio= new_audio[segment["start"]*1000:segment["end"]*1000]
                new_audio.export(os.path.join(output_audio_folder, f"{ulid_str}.mp3"), format="mp3")
                transcript_df = pd.concat([transcript_df, pd.DataFrame([{"ulid": ulid_str, "text": segment["text"].strip()}])], ignore_index=True)
            transcript_df.to_csv(os.path.join(batch_csv_folder, f"{item}.csv"), index=False)
            df = pd.concat([df, transcript_df], ignore_index=True)
    print("------------------------------")
    print(df.tail(5))
    print("------------------------------")
    print(f"{df.shape} - total dataframe shape")
    print(f"{index} - current index")
    print(f"{item} = current item")

df.to_csv('all_data.csv', index=False)
