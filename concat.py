import json
import os 
path = "./outs/"

arr_list = [
    os.path.splitext(f)[0] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
]
# arr_list=["bisaya core", "bisaya valorant", "bisaya vs tagalog trashtalk", "bisayavstagalog", "bobo", "cebuano swear", "duterte", "filipino cursing", "filipino trashtalk", "filipinovalorant", "fliptop battle league", "fliptopbattle", "kabobohan","malutong na mura", "mura", "pisting yawa", "potang", "put4angina", "tarantado", "wrecker"]

print("keywords #" +str(len(arr_list)))

batch = "batch1"
overall_data = []
for i in arr_list:
    print(f"-------------------{i}------------------------")
    with open("outs/"+i+".json", "r") as out:
        data = json.loads(out.read())
        overall_data = overall_data + data
        print(len(overall_data))

unique_data = list(set(overall_data))
print(len(unique_data))

with open(batch+".json", "w") as out_file:
    json.dump(unique_data, out_file)