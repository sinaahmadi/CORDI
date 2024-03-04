import os
import re
import srt
import json
from pydub import AudioSegment
from klpt.preprocess import Preprocess

# Sina Ahmadi - April 2023

preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Latin")

with open("utils/character_list_M.txt", "r") as f:
	characters_M = f.read().splitlines()
with open("utils/character_list_F.txt", "r") as f:
	characters_F = f.read().splitlines()

def process(text, filename, audio_file, remove_description=True, audio_format=".wav", export_directory = "content/segments/"):
	# normalize & standarize the text
	text = preprocessor_ckb.preprocess(text)
	text = text.replace("‎", "").replace("”", " ").replace("“", " ").replace(";", " ").replace("؛", " ")

	subs = list(srt.parse(text))
	new_subs, meta_json = list(), list()

	for sub in subs:
		sub_name = list()

		if len(sub.content) == 0 or len("".join(sub.content.split())) == 0:
			# remove empty segments
			continue
		
		else:
			# metadata
			sub_meta = {
				"ID": str(sub.index),
				"gender": "NA", 
				"age": "NA", 
				"character_name": "NA",
				"text": "",
				"text_original": "",
				"start": "",
				"end": ""
			}
			sub_meta.update({"audio": export_directory + filename + "/" + sub_meta["ID"] + "." + "ogg"})

			# remove ⁃ and punctuations at the beginning of the segments as in "⁃ مارف"
			sub.content = sub.content.replace(",", " ")
			sub.content = re.sub(r'^⁃', ' ', sub.content.strip())
			sub.content = re.sub(r'^:', ' ', sub.content.strip())
			sub.content = re.sub(r'^\.', ' ', sub.content.strip())
			sub.content = re.sub(r'^:', '', sub.content.strip())
			sub.content = re.sub(r':$', '', sub.content.strip())
			sub.content = re.sub(r'^\،', ' ', sub.content.strip())
			sub.content = re.sub(r'؟+', ' ', sub.content.strip())
			sub.content = re.sub(r'\.+', ' ', sub.content.strip())
			sub.content = re.sub(r'!+', ' ', sub.content.strip())
			sub.content = re.sub(r'،$', ' ', sub.content.strip())
			sub.content = sub.content.replace("::", ":")
			sub.content = sub.content.replace("،:", ":")
			sub.content = " ".join(sub.content.split())

			if remove_description and sub.content.strip()[0] == "(" and sub.content.strip()[-1] == ")":
				# remove descriptive segements in parantheses including گۆرانی
				continue

			# find character specified at the beginning of a segment with :"
			if ":" in sub.content:
				ch_name = re.findall(r'^.*:', sub.content)[0]
				if len(ch_name) and len(ch_name) < 12:
					sub_meta["character_name"] = ch_name.replace(":", "").strip()

				if "پیاگ" in sub_meta["character_name"] or \
						"پیاو" in sub_meta["character_name"] or \
						"ئاغا" in sub_meta["character_name"] or \
						"باوک" in sub_meta["character_name"] or \
						"مام" in sub_meta["character_name"] or \
						"پیا" in sub_meta["character_name"] or \
						"پۆلیسی" in sub_meta["character_name"] or \
						"پۆلس" in sub_meta["character_name"] or \
						"پاوی" in sub_meta["character_name"] or \
						"پئاو" in sub_meta["character_name"] or \
						"پایگ" in sub_meta["character_name"] or \
						"پاگ" in sub_meta["character_name"] or \
						"کوڕی" in sub_meta["character_name"] or \
						"گەنج" in sub_meta["character_name"] or \
						"یاوی" in sub_meta["character_name"] or \
						True in [True for c in characters_M if c in sub_meta["character_name"]]:
					sub_meta["gender"] = "M"
					sub_meta["age"] = "A"

				elif "ئافرەت" in sub_meta["character_name"] or \
						"ژن" in sub_meta["character_name"] or \
						"کچی" in sub_meta["character_name"] or \
						True in [True for c in characters_F if c in sub_meta["character_name"]]:
					sub_meta["gender"] = "F"
					sub_meta["age"] = "A"

				elif "کچ" in sub_meta["character_name"]:
					sub_meta["gender"] = "F"
					sub_meta["age"] = "C"

				elif "کوڕ" in sub_meta["character_name"] or "کور" in sub_meta["character_name"]:
					sub_meta["gender"] = "M"
					sub_meta["age"] = "C"

				elif "منداڵ" in sub_meta["character_name"] or "منال" in sub_meta["character_name"] or "مناڵ" in sub_meta["character_name"]:
					sub_meta["age"] = "C"


			sub.content = re.sub(r'^.*:', '', sub.content.strip()).strip()
			sub_meta["text"] = sub.content
			sub_meta["text_original"] = sub.content

			if len(sub.content) > 1:
				# this segment is valid
				new_subs.append(srt.Subtitle.to_srt(sub))
				meta_json.append(sub_meta)

				# extract the audio
				if not os.path.exists(export_directory + filename):
					os.makedirs(export_directory + filename)
				
				if audio_format == 'mp3':
					audio = AudioSegment.from_mp3(audio_file)
				elif audio_format == "wav":
					audio = AudioSegment.from_wav(audio_file)
				elif audio_format == "m4a":
					audio = AudioSegment.from_file(audio_file)

				sub_meta["start"] = sub.start.total_seconds() * 1000
				sub_meta["end"] = sub.end.total_seconds() * 1000
				audio_segment = audio[sub_meta["start"]: sub_meta["end"]]	
				audio_segment.export(export_directory + filename + "/" + sub_meta["ID"] + ".ogg", format='ogg')

	print("# segments: ", len(subs))
	print("# clean segments: ", len(new_subs))
	
	return "".join(new_subs), meta_json # return the clean srt file without characters and metadata
	
text = os.listdir('content/text_original/')
with open("metadata.json", "r") as f:
	data = json.load(f)["CORDI"]

for i in data:
	if int(i) >= 278 and data[i]["is_synched"]:
		print("Processing " + i + "...")

		with open(data[i]["text"], "r") as f:
			text, meta = process(f.read(), i, data[i]["audio"], audio_format=data[i]["audio"].split(".")[-1])
		
		with open('content/text/' + i + ".srt", "w") as f:
			f.write(text)		
		
		with open('content/segments/%s.json'%i, 'w', encoding='utf-8') as f:
		 	json.dump(meta, f, ensure_ascii = False, indent=4)

