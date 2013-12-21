#!/bin/python3
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
from grammar import is_zh

def n_grams(text_buffer, N, top):
    text = ''.join([w for w in ''.join([l for l in text_buffer]) if is_zh(w)])
    cnt = defaultdict(int)
    p = [defaultdict(float) for x in range(0, N)]
    tot = len(text)
    for w in iter(text):
        cnt[w] += 1
    for w in iter(text):
        p[0][w] = cnt[w]/float(tot)
    for i in range(1, N):
        for j in range(0, len(text) - i):
            sub = text[j:j+i+1]
            if sub not in cnt:
                cnt[sub] = text.count(sub)
            p[i][sub] = cnt[sub]/float(cnt[sub[:-1]])*p[i-1][sub[:-1]]
    for i in range(0, N):
        for pr in sorted(p[i], key=lambda x: p[i][x], reverse=True)[:top]:
            print(pr, p[i][pr], cnt[pr])

n_grams(open(sys.argv[1], "r"), int(sys.argv[2]), int(sys.argv[3]))
