#!/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
from collections import defaultdict

from grammar import is_zh


def n_grams(text_buffer, N=2, top=100):
    if type(text_buffer) is list:
        text = ''
        for _file in text_buffer:
            with open(_file, "r") as _input:
                text += ''.join([w for w in ''.join([l for l in _input]) if is_zh(w)])
    else:
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
    result = []
    for i in range(0, N):
        tuple_list = []
        for pr in sorted(p[i], key=lambda x: p[i][x], reverse=True):
            tuple_list.append((pr, p[i][pr], cnt[pr]))
        result.append(tuple_list)
        # output each grams in top i
        print (i+1, "grams result")
        print ("\n".join([str(_) for _ in tuple_list[:top]]))

    return result


if __name__ == "__main__":
    # count 2 grams in all text
    import os
    text_files = ["text/article/" + f for f in os.listdir("text/article/")]
    for _ in text_files:
        print (_)
        n_grams(open(_, "r"), top=10)
