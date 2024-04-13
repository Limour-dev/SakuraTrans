# mamba create -n SakuraTrans python=3.10 langdetect requests -c conda-forge
from langdetect import detect_langs, DetectorFactory
from transJa import transJa as _transJa

DetectorFactory.seed = 0


def get_all_files_in_directory(directory, ext=''):
    import os
    import re
    custom_sort_key_re = re.compile('([0-9]+)')

    def custom_sort_key(s):
        # 将字符串中的数字部分转换为整数，然后进行排序
        return [int(x) if x.isdigit() else x for x in custom_sort_key_re.split(s)]

    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(ext):
                file_path = os.path.join(root, file)
                all_files.append(file_path)
    return sorted(all_files, key=custom_sort_key)


def detect_zh_ja_fix(_sl, _delta=10):
    for _i in range(len(_sl)):
        _st = max(0, _i - _delta)
        _ed = min(len(_sl), _i + _delta)
        _ratio = sum(_sl[_j] for _j in range(_st, _ed)) / (_ed - _st)
        if _sl[_i] == 0:  # zh
            if _ratio > 0.8:
                _sl[_i] = 1
        else:  # ja
            if _ratio < 0.2:
                _sl[_i] = 0
    return _sl


def detect_zh_ja(_s: str):
    _s = _s.strip()
    _langs = detect_langs(_s)
    _lang = _langs[0]
    if not (_lang.lang.startswith('ja') and _lang.prob > 0.95):
        return 0
    print(_langs, _s)
    return 1


def transJa(_s: str):
    _s = _s.strip()
    _s_t = _transJa(_s)
    print(_s, _s_t)
    return _s_t.strip() + '\n'


_a = get_all_files_in_directory(r'D:\datasets\test', ext='.txt')

for _path in _a:
    with open(_path, 'r', encoding='utf-8') as _f:
        _lines = _f.readlines()
    _l_d = []
    for _line in _lines:
        if '：' in _line:
            _idx = _line.index('：')
            n = _line[:_idx]
            _l_d.append(detect_zh_ja(_line[_idx + 1:]))
        else:
            _l_d.append(detect_zh_ja(_line))
    _l_d = detect_zh_ja_fix(_l_d)
    with open(_path + '.trans', 'w', encoding='utf-8') as _f:
        for i in range(len(_l_d)):
            _line = _lines[i]
            if _l_d[i] == 0:  # zh
                _f.write(_line)
            else:  # ja
                if '：' in _line:
                    _idx = _line.index('：')
                    n = _line[:_idx]
                    _f.write(n + '：' + transJa(_line[_idx + 1:]))
                else:
                    _f.write(transJa(_line))
