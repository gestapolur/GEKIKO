# -*- coding: utf-8 -*-
import sys

is_zh = (lambda x: True if 19968 <= ord(x) <= 40908 else False)

def n_grams(text_buffer):
    text = [line.decode('utf-8') for line in text_buffer]
    tot = [w for w in text[0] if is_zh(w)]
    print tot
    for w in [w for w in text[0] if is_zh(w)]:
        print w/tot

n_grams(open(sys.argv[1], "r"))
