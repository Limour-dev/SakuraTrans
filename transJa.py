import requests
import traceback

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
        "max_tokens": 1000,
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
    return ''


def transJa(_s: str):
    for i in range(3):
        try:
            retn = transJa_One(_s)
            if retn:
                return retn
        except:
            print(traceback.format_exc())
    return _s
