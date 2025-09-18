import requests
import yt_dlp
import os
import json
import ulid

output_folder = "audio_data_v2"
batch_name = "batch1.json"

url_list = []
with open(batch_name, "r") as out:
    data = json.loads(out.read())
    url_list =  data
    print(len(url_list))
ulid_set = set()
n = 4500
for url in url_list[4000:5000]:
    ulid_str = str(ulid.ULID())
    
    print(ulid_str)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = os.path.join(output_folder, f"{ulid_str}.mp3")
        with open(filename, "wb") as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)
        ulid_set.add(ulid_str)  
        print(f"Downloaded: {filename} {len(ulid_set)}")
    # try:
    #     ydl_opts = {
    #         'format': 'bestaudio/best',
    #         'outtmpl': os.path.join(output_folder, ulid_str+'.%(ext)s'),
    #         'quiet': False,
    #         'noplaylist': True,
    #         'postprocessors': [{
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192',
    #         }],
    #     }
    #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #         ydl.download([url])
    #     ulid_set.add(ulid_str)  
    except Exception as e:
        print(f"Failed to download {url}: {e}")

print(len(ulid_set))
with open(batch_name+str(n)+"_ulid.json", "w") as out_file:
    json.dump(list(ulid_set), out_file)