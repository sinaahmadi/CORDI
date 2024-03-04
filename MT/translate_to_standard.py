import json
from klpt.preprocess import Preprocess
from klpt.tokenize import Tokenize
from klpt.stem import Stem


'''
	This script converts a text written in one of the following dialects of Central Kurdish into Standard Central Kurdish:
		- Sulaymaniyah (SL)
		- Sanandaj (SN)
		- Erbil (HW)
		- Mahabad (MH)

	The script relies on the following two steps to do so:
	# Applying morphosyntactic rules using a morphological analyzer
	# Adding dialectal lexical variations

	It reverses the functionality of `translate_to_dialect.py`

	Last updated on October 14th, 2023
	Sina Ahmadi (ahmadi.sina@outlook.com)

'''
preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Latin")
tokenizer_ckb = Tokenize("Sorani", "Arabic")
stemmer = Stem("Sorani", "Arabic")

# read the input in the standard variety of the language
with open('morphosyntactic_variations.json') as f:
     morphosyntactic = json.load(f)

with open('dialect_lexicon.json') as f:
	lexicon = json.load(f)

with open('terms.json') as f:
	term = json.load(f)

def normalize_morphosyntactic_rules(text, dialect):
	new_text = list()
	# Let's tokenize it by space for now. To further analyze the impact of a correct tokenization.
	# tokens = tokenizer_ckb.word_tokenize(text, separator=" ", mwe_separator=" ", keep_form=True)
	tokens = text.split()
	for t in tokens:
		new_t = t

		# Adpositional suffixes -da, -ra & -ewe
		if dialect == "SL":
			if t[-1] == "ا":
				analysis = stemmer.analyze(t[:-1] + "دا")
				if len(analysis) and analysis[0]["suffixes"] in ["دا"]:
					new_t = t[:-1] + "دا"

		elif dialect == "SN":
			if t[-1] == "ا":
				analysis = stemmer.analyze(t[:-1] + "دا")
				if len(analysis) and analysis[0]["suffixes"] in ["دا"]:
					new_t = t[:-1] + "دا"

			elif len(t) > 2 and t[-2:] == "ەو":
				analysis = stemmer.analyze(t[:-2] + "ەوە")
				if len(analysis):
					new_t = t[:-2] + "ەوە"

			elif len(t) > 3 and t[-3:] == "گەل":
				analysis = stemmer.analyze(t[:-3] + "ان")
				if len(analysis):
					new_t = t[:-3] + "ان"

			elif len(t) > 2 and t[-2:] == "گە":
				analysis = stemmer.analyze(t[:-2] + "ووە")
				if len(analysis):
					new_t = t[:-2] + "ووە"

		elif dialect == "HW":
			if len(t) > 2 and t[-2:] == "ەک":
				analysis = stemmer.analyze(t[:-2] + "ێک")
				if len(analysis):
					new_t = t[-2:] + "ێک"

			elif len(t) > 2 and t[-2:] == "یە":
				analysis = stemmer.analyze(t[:-2] + "ووە")
				if len(analysis):
					new_t = t[-2:] + "ووە"

		# Verbal progressive prefix (e or de)
		if dialect == "SL" or dialect == "SN":
			search_for = "ئە"
		else:
			search_for = "دە"

		analysis = stemmer.analyze(new_t)
		if len(analysis) and analysis[0]["pos"] == ["verb"]:
			if search_for in analysis[0]["prefixes"]:
				new_t = analysis[0]["prefixes"].replace(search_for, "دە") + new_t.replace(analysis[0]["prefixes"], "")
		new_text.append(new_t)

	return " ".join(new_text)

def transform(text, dialect):
	new_text = list()

	other_dialect = "MH"
	if dialect == "MH" or dialect == "HW":
		other_dialect = "SN"

	for i in text.split():
		checked_flag = False
		# check the mappings
		for j in morphosyntactic:
			if morphosyntactic[j][dialect] == i:
				new_text.append(j)
				checked_flag = True
				break

		if not checked_flag:
			for j in lexicon:
				if lexicon[j][dialect] == i:
					new_text.append(j)
					checked_flag = True
					break

		if not checked_flag:
			for j in term:
				if term[j][dialect] == i:
					new_text.append(j)
					checked_flag = True
					break

		if not checked_flag:
			# apply morphosyntactic rules
			new_text.append(i)

	return normalize_morphosyntactic_rules(" ".join(new_text), dialect)

# print(normalize_morphosyntactic_rules("ئەکەمەو تارانا گوڵگەل کردگە ", dialect="SN"))
# print(transform("ئەکەمەو تارانا گوڵگەل کردگە ", dialect="SN"))

# convert text in one of the dialects into Standard Central Kurdish

# configs = {
# 	"SL": "gold-standard/ckb-sl.txt",
# 	"SN": "gold-standard/ckb-sn.txt",
# 	"HW": "gold-standard/ckb-hw.txt",
# 	"MH": "gold-standard/ckb-mh.txt"
# }

# for c in configs:
# 	print(c)
# 	with open(configs[c], "r") as f:
# 		input_file = f.read().splitlines()

# 	standardized = list()
# 	for i in input_file:
# 		standardized.append(transform(i, c))

# 	with open("translations/standardized_ckb_" + c.lower() + ".txt", "w") as f:
# 		f.write("\n".join(standardized))

