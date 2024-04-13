import requests
import traceback
import re

reg1 = re.compile(r'(.)\1{3,}')


def reg1_replace(match):
    return match.group(1) * 3


reg2 = re.compile(r'(.{2,}?)\1{2,}')


def reg2_replace(match):
    return match.group(1)


def removeRep(_s:str):
    retn = reg1.sub(reg1_replace, _s)
    retn = reg2.sub(reg2_replace, retn)
    return retn


header = {
    'Content-Type': 'application/json',
    'Authorization': ''
}

url = r''


def transJa_One(_s: str):
    data = {
        "model": "sukinishiro",
        "messages": [
            {
                "role": "system",
                "content": "你是一个轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将日文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。"
            },
            {
                "role": "user",
                "content": f"将下面的日文文本翻译成中文：{_s}"
            }
        ],
        "temperature": 0.1,
        "top_p": 0.3,
        "max_tokens": int(len(_s) * 1.5) + 10,
        "frequency_penalty": 0,
        "do_sample": True,
        "top_k": 40,
        "num_beams": 1,
        "repetition_penalty": 1
    }
    r = requests.post(url, headers=header, json=data, timeout=120)
    r = r.json()
    if 'choices' in r:
        return r['choices'][0]['message']['content']
    else:
        print(r)
    return ''


def transJa(_s: str):
    _s = removeRep(_s)
    for i in range(3):
        try:
            retn = transJa_One(_s)
            if retn:
                retn = removeRep(retn)
                if retn.startswith('「') and not retn.endswith('」'):
                    retn += '」'
                return retn
        except:
            print(traceback.format_exc())
    return _s
