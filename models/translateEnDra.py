from multiprocessing.context import _force_start_method
from unittest import result
from transformers import MarianTokenizer, MarianMTModel



def translateMul2EnText(text):
    model_name = f"Helsinki-NLP/opus-mt-mul-en"

    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    batch = tokenizer([f"{text}"], return_tensors="pt")

    generated_ids = model.generate(**batch)

    results = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    return results




def translateEn2MulText(text, lang):
    model_name = f"Helsinki-NLP/opus-mt-en-mul"

    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    batch = tokenizer([f">>{lang}<<{text}"], return_tensors="pt")

    generated_ids = model.generate(**batch)

    results = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    return results



if __name__=="__main__":
    print(translateEn2MulText("Al Qaeda leader al-Zawahiri killed in drone strike: Was hiding in Kabul for 12 months, Biden said - we found and killed; Taliban flare up", "hin"))


