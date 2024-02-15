from google.transliteration import transliterate_text
import re
language = {
    "Tamil":"ta",
    "Malayalam":"ml",
    "Kannada":"kn",
    "Hindi":"hi",
    "Gujarati":"gu",
    "Bengali":"bn",
    "Punjabi":'pa'
}


def transliteration_language(text, lang):
    lan_code = language[lang]
    result = transliterate_text(text, lang_code=lan_code)
    return result


import http.client
import json

def request(input,lang):
    conn = http.client.HTTPSConnection('inputtools.google.com')
    lan = '{}-t-i0-und'.format(language[lang])
    conn.request('GET', '/request?text=' + input + '&itc=' + lan + '&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=test')
    res = conn.getresponse()
    return res

def driver(input,lang):
    output = ''
    if ' ' in input:
        input = input.split(' ')
        for i in input:
            res = request(input = i,lang=lang)
            #print(res.read() )
            res = res.read()
            if i==0:
                output = str(res, encoding = 'utf-8')[14+4+len(i):-31]
            else:
                output = output + ' ' + str(res, encoding = 'utf-8')[14+4+len(i):-31]
    else:
        res = request(input = input, lang=lang)
        res = res.read()
        output = str(res, encoding = 'utf-8')[14+4+len(input):-31]
    return output


