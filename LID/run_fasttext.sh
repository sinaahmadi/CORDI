#!/bin/bash

# Just run it: bash run_fasttext.sh

echo "Training the model..." data
./fastText-0.9.2/fasttext  supervised -input data/train.txt -output models/CKB_dialects_model -dim 64 -minn 2 -maxn 6 -loss hs  -epoch 25  -lr 1.0

echo "Compressing..."
./fastText-0.9.2/fasttext quantize -input data/train.txt -output models/CKB_dialects_model -qnorm -cutoff 50000 -retrain

echo "Testing the model..."
./fastText-0.9.2/fasttext test models/CKB_dialects_model.bin data/test.txt
./fastText-0.9.2/fasttext test models/CKB_dialects_model.bin data/test.txt 2
./fastText-0.9.2/fasttext test models/CKB_dialects_model.bin data/test.txt 3
./fastText-0.9.2/fasttext test models/CKB_dialects_model.bin data/test.txt 4

./fastText-0.9.2/fasttext predict models/CKB_dialects_model.bin data/test.txt 4 > models/predict.txt

echo "Testing with lid.176..."
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin data/test.txt
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin data/test.txt 2
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin data/test.txt 3
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin data/test.txt 4

./fastText-0.9.2/fasttext predict fastText-0.9.2/lid.176.bin data/test.txt 4 > models/predict-lid.176.txt

echo "Testing with Perso-Arabic LID"
./fastText-0.9.2/fasttext test /Users/sina/My_GitHub/PersoArabicLID/models/LID_model_merged.ftz data/test.txt
./fastText-0.9.2/fasttext test /Users/sina/My_GitHub/PersoArabicLID/models/LID_model_merged.ftz data/test.txt 2
./fastText-0.9.2/fasttext test /Users/sina/My_GitHub/PersoArabicLID/models/LID_model_merged.ftz data/test.txt 3
./fastText-0.9.2/fasttext test /Users/sina/My_GitHub/PersoArabicLID/models/LID_model_merged.ftz data/test.txt 4

./fastText-0.9.2/fasttext predict /Users/sina/My_GitHub/PersoArabicLID/models/LID_model_merged.ftz data/test.txt 4 > models/predict_Perso-Arabic-LID.txt

echo "Testing with Kurdish LID"
./fastText-0.9.2/fasttext test /Users/sina/My_GitHub/KurdishLID/models/KLID_model.ftz data/test.txt
./fastText-0.9.2/fasttext test /Users/sina/My_GitHub/KurdishLID/models/KLID_model.ftz data/test.txt 2
./fastText-0.9.2/fasttext test /Users/sina/My_GitHub/KurdishLID/models/KLID_model.ftz data/test.txt 3
./fastText-0.9.2/fasttext test /Users/sina/My_GitHub/KurdishLID/models/KLID_model.ftz data/test.txt 4

./fastText-0.9.2/fasttext predict /Users/sina/My_GitHub/KurdishLID/models/KLID_model.ftz data/test.txt 4 > models/predict_Kurdish-LID.txt


