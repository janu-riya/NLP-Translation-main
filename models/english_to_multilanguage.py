# !pip install transformers

# https://colab.research.google.com/drive/11em-WPn8jUyoCONPPsKm2wJk0hKnGwqR?usp=sharing#scrollTo=upBfRlM6mAt1

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def eng_to_mul(eng_txt, language):

    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
    tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

    language_dictionary = {
                          'Tamil': 'tam_Taml','Telugu': 'tel_Telu', 'Malayalam': 'mal_Mlym', 
                          'Hindi': 'hin_Deva', 'Urdu': 'urd_Arab', 'Kannada': 'kan_Knda',
                          }

    c_lang = language_dictionary[language]

    translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang="eng_Latn", tgt_lang= c_lang , max_length = 2000)

    result_txt = translator(eng_txt)

    return result_txt
