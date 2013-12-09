#!/bin/python3
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
is_zh = (lambda x: True if 19968 <= ord(x) <= 40908 else False)

def n_grams(text_buffer, N, top):
    text = ''.join([w for w in ''.join([l for l in text_buffer]) if is_zh(w)])
    cnt = defaultdict(int)
    p = [defaultdict(float) for x in range(0, N)]
    tot = len(text)
    for w in iter(text):
        p[0][w] = text.count(w)/float(tot)
    for i in range(1, N):
        for j in range(0, len(text) - i):
            sub = text[j:j+i+1]
            p[i][sub] = text.count(sub)/float(text.count(sub[:-1]))*p[i-1][sub[:-1]]
    for i in range(0, N):
        for pr in sorted(p[i], key=lambda x: p[i][x], reverse=True)[:top]:
            print(pr, p[i][pr])

n_grams(open(sys.argv[1], "r"), int(sys.argv[2]), int(sys.argv[3]))
