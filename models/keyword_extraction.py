from keybert import KeyBERT

def keyword(text, language):
    doc = text
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(doc)
    lis = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 1), stop_words=None)
    result = []
    for i in lis:
        result.append(i[0])

    return result
