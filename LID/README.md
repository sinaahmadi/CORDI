## Language identification for Central Kurdish Varieties

Language identification (LID) is the task of identifying the language in which a text is written. In our paper, we focus on the identification of dialects in CORDI. 

We provide the [CKB\_dialects\_model.ftz](CKB_dialects_model.ftz) model for dialect identification. This model is trained on CORDI data using `fastText`. You can run the model in Python or on command-line by installing the `fastText`library as described at [https://fasttext.cc/docs/en/support.html](https://fasttext.cc/docs/en/support.html) as follows:

```python
>>> import fasttext
>>> model = fasttext.load_model("CKB_dialects_model.ftz")

# Central Kurdish
>>> model.predict("لەزۆربەی یارییەکان گوڵ تۆمار دەکات") # Sulaymaniyah
(('__label__ckb-slm',), array([0.57287467]))
>>> model.predict("لەزۆربەی یارییەکان گوڵ تۆمار دەکات", k=3) # Three most probable predictions
(('__label__ckb-slm', '__label__ckb-mhb', '__label__ckb-hwl'), array([0.57287467, 0.28914055, 0.13782322]))
>>> model.predict("ئەم گشتە قسە و باسە چەس؟")
(('__label__ckb-snn',), array([0.99485528])) # Sanandaj
>>> model.predict("دری من باسی چ دەکەی")
(('__label__ckb-hwl',), array([0.95625365])) # Erbil
```

The model is trained on the following varieties (with their dialect code in parentheses):

- Sulaymaniyah (`__label__ckb-slm`)
- Sanandaj (`__label__ckb-snn`)
- Erbil (`__label__ckb-hwl`)
- Mahabad (`__label__ckb-mhb`)
- Kalar (`__label__ckb-klr`)


### See also:
You can use this model along with [PALI](https://github.com/sinaahmadi/PersoArabicLID) and [KurdishLID](https://github.com/sinaahmadi/KurdishLID) models.