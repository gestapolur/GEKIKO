#!/bin/python3
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
is_zh = (lambda x: True if 19968 <= ord(x) <= 40908 else False)

def output_morphe(text_buffer, N=2):
    text = ''.join([w for w in ''.join([l for l in text_buffer]) if is_zh(w)])
    cnt = defaultdict(int)
    for i in range(0, N):
        for j in range(0, len(text) - i):
            cnt[text[j:j+i+1]] += 1
    for i in range(0, N):
        length = len([c0 for c0 in cnt if len(c0) == i+1])
        for c in sorted([c0 for c0 in cnt if len(c0) == i+1],
                        key=lambda x: cnt[x], reverse=True)[:int(length/3)]:
            print(c, cnt[c])
        print("%s char totally." % length)

output_morphe(open(sys.argv[1], "r"))
