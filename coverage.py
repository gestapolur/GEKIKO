#!/bin/python3
# -*- coding: utf-8 -*-
import sys
from grammar import is_zh

def cnt(text_buffer, tagged_word_buffer):
    text = ''.join([w for w in ''.join([l for l in text_buffer]) if is_zh(w)])
    tagged_word = set()
    tot = 0
    for w in tagged_word_buffer:
        w = w[:-1]
        key, weight, tag = w.split(' ')
        tagged_word.add(key)
    for t in text:
        if t in tagged_word:
            tot += 1
    print("coverage ratio:%s" % (float(tot)/len(text)))


cnt(open(sys.argv[1], 'r'),
    open(sys.argv[2], 'r'))
