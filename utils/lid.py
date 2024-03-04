import json
with open("/Users/sina/My_GitHub/CORDI/metadata.json", "r") as f:
	metadata = json.load(f)["CORDI"]

for dialect in ["Silêmanî", "Hewlêr", "Kalar", "Sine", "Mehabad", "Serdeşt"]:
	all_text = list()
	for i in metadata:
		if metadata[i]["Dialect"] == dialect:
			with open(metadata[i]["text"].replace("text_original", "text"), "r") as f:
				all_text.append(f.read())

	with open("LID_data/" + dialect + ".txt", "w") as f:
		f.write("\n".join(all_text))