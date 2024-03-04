import json
from klpt.preprocess import Preprocess
from klpt.tokenize import Tokenize
from klpt.stem import Stem


'''
	This script converts a text written in Standard Central Kurdish into one of the following dialects:
		- Sulaymaniyah (SL)
		- Sanandaj (SN)
		- Erbil (HW)
		- Mahabad (MH)

	The script relies on the following two steps to do so:
	# Applying morphosyntactic rules using a morphological analyzer
	# Adding dialectal lexical variations

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

def apply_morphosyntactic_rules(text, dialect):
	new_text = list()
	prog_prefix = {"SL": "ئە", "SN": "ئە", "MH": "دە", "HW": "دە"}
	adp_suffixes = {
	"SL": {
			"دا": "ا",
			"ڕا": "ەوە",
			"ەوە": "ەوە"
		},
	"SN": {
		"دا": "ا",
		"ڕا": "ەو",
		"ەوە": "ەو"
		}
	}

	# Let's tokenize it by space for now. To further analyze the impact of a correct tokenization.
	# tokens = tokenizer_ckb.word_tokenize(text, separator=" ", mwe_separator=" ", keep_form=True)
	tokens = text.split()
	for t in tokens:
		analysis = stemmer.analyze(t)
		new_t = t

		# Verbal progressive prefix (e or de)
		if dialect == "SL" or dialect == "SN":
			search_for = "دە"
		else:
			search_for = "ئە"

		if len(analysis) and analysis[0]["pos"] == ["verb"]:
			if search_for in analysis[0]["prefixes"]:
				new_t = analysis[0]["prefixes"].replace(search_for, prog_prefix[dialect]) + t.replace(analysis[0]["prefixes"], "")

		# Adpositional suffixes -da, -ra & -ewe
		if dialect == "SL" or dialect == "SN":
			if len(analysis) and analysis[0]["suffixes"] in ["دا", "ڕا", "ەوە"]:
				new_t = t.replace(analysis[0]["suffixes"], "") + adp_suffixes[dialect][analysis[0]["suffixes"]]

		# Article markers
		if dialect == "HW":
			if len(analysis) and analysis[0]["suffixes"] in ["ێک"]:
				new_t = t.replace(analysis[0]["suffixes"], "") + "ەک"
			if len(analysis) and analysis[0]["suffixes"] in ["ووە"]:
				new_t = t.replace(analysis[0]["suffixes"], "") + "یە"

		if dialect == "SN":
			if len(analysis) and analysis[0]["suffixes"] in ["ان"]:
				new_t = t.replace(analysis[0]["suffixes"], "") + "گەل"
			if len(analysis) and analysis[0]["suffixes"] in ["ووە"]:
				new_t = t.replace(analysis[0]["suffixes"], "") + "گە"

		new_text.append(new_t)

	# print(" ".join(new_text))
	return " ".join(new_text)

def transform(text, dialect):
	new_text = list()
	# apply morphosyntactic rules
	text = apply_morphosyntactic_rules(text, dialect)

	other_dialect = "MH"
	if dialect == "MH" or dialect == "HW":
		other_dialect = "SN"

	for i in text.split():
		# check the mappings
		if i in morphosyntactic:
			new_text.append(morphosyntactic[i][dialect])
		elif i in lexicon:
			new_text.append(lexicon[i][dialect])
		
		# check if verbs without changing their prefix exist in the lexicon
		elif apply_morphosyntactic_rules(i, other_dialect) in morphosyntactic:
			new_text.append(morphosyntactic[apply_morphosyntactic_rules(i, other_dialect)][dialect])
		elif apply_morphosyntactic_rules(i, other_dialect) in lexicon:
			new_text.append(lexicon[apply_morphosyntactic_rules(i, other_dialect)][dialect])
		
		# no replacement needed
		else:
			new_text.append(i)

	# replace phrases in the dictionary, aka words containing a space, replace them at the phrase level
	new_text = " ".join(new_text)
	for i in morphosyntactic:
		if " " in i:
			new_text = new_text.replace(i, morphosyntactic[i][dialect])

	# replace terms and words imposed by the administration
	for i in term:
		new_text = new_text.replace(i, term[i][dialect])

	return new_text

# apply_morphosyntactic_rules
# output = transform("ژن زیز ئەبێ ژن عاجز بوو . پیاو تووڕە دەبێ .", dialect="SN")
# print(output)
# print(transform("ئەوە چییە بۆ منت ناردووە لە ماڵدا لە لای ئەوان و پیاوێک و ژنان مەسعەد ؟", dialect="HW"))
# print(transform("ئەوە چییە بۆ منت ناردووە لە ماڵدا لە لای ئەوان و پیاوێک و ژنان مەسعەد ؟", dialect="SN"))

# ckb-sn.txt
# ckb-sl.txt
# ckb-mh.txt
# ckb-hw.txt

# NLLB
# with open("translations/en_translated.txt", "r") as f:
# 	input_file = preprocessor_ckb.preprocess(f.read()).splitlines()

# for c in ["SL", "SN", "HW", "MH"]:
# 	synthetic = list()
# 	for i in input_file:
# 		synthetic.append(transform(i, c))

# 	with open("translations/en_translated_ckb_%s_synthetic.txt"%c, "w") as f:
# 		f.write("\n".join(synthetic))

# Google
with open("translations/en_translated_Google.txt", "r") as f:
	input_file = preprocessor_ckb.preprocess(f.read()).splitlines()

for c in ["SL", "SN", "HW", "MH"]:
	synthetic = list()
	for i in input_file:
		synthetic.append(transform(i, c))

	with open("translations/en_translated_ckb_%s_synthetic_Google.txt"%c, "w") as f:
		f.write("\n".join(synthetic))



