import json
import os

# Sina Ahmadi - November 2022

with open("metadata.tsv", "r") as f:
    tsv = f.read().splitlines()[1:]

audio = os.listdir('content/audio')
text = os.listdir('content/text_original')
video = os.listdir('content/video')

# metadata_json = list()
metadata_json = dict()
for i in tsv:
    
    metadata_json.update(
        {i.split("\t")[0]: {
                "Dialect": i.split("\t")[1],
                "Title_ckb_arab": i.split("\t")[2],
                "Title_ckb_latn": i.split("\t")[3],
                "Episode": i.split("\t")[4],
                "Episode_ckb_arab": i.split("\t")[5],
                "Episode_ckb_latn": i.split("\t")[6],
                "Type": i.split("\t")[7],
                "Genre": i.split("\t")[8],
                "is_synched": i.split("\t")[9],
                "Transcriber": i.split("\t")[10],
                "Comment": i.split("\t")[11],
                "text": "",
                "audio": "",
                "video": ""
         }
        }
    )

    if metadata_json[i.split("\t")[0]]["is_synched"] == "TRUE":
        metadata_json[i.split("\t")[0]]["is_synched"] = True
    else:
        metadata_json[i.split("\t")[0]]["is_synched"] = False


    if i.split("\t")[0] + ".m4a" in audio:
        metadata_json[i.split("\t")[0]].update({"audio": "content/audio/" + i.split("\t")[0] + ".m4a"})
    elif i.split("\t")[0] + ".wav" in audio:
        metadata_json[i.split("\t")[0]].update({"audio": "content/audio/" + i.split("\t")[0] + ".wav"})
    else:
        metadata_json[i.split("\t")[0]].update({"audio": ""})

    if i.split("\t")[0] + ".srt" in text:
        metadata_json[i.split("\t")[0]].update({"text": "content/text_original/" + i.split("\t")[0] + ".srt"})

    if i.split("\t")[0] + ".mp4" in video:
        metadata_json[i.split("\t")[0]].update({"video": "content/video/" + i.split("\t")[0] + ".mp4"})
    elif i.split("\t")[0] + ".mov" in video:
        metadata_json[i.split("\t")[0]].update({"video": "content/video/" + i.split("\t")[0] + ".mov"})
    else:
        metadata_json[i.split("\t")[0]].update({"video": ""})


with open('metadata.json', 'w', encoding='utf-8') as f:
    json.dump({"CORDI": metadata_json}, f, ensure_ascii = False, indent=4)


