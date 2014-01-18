#!/bin/python3
# -*- coding: utf-8 -*-
"""
this module caculate coverage rate by reading text from argv[1] and reading

tagged chars from argv[2] 
"""

import sys
from grammar import is_zh

def cnt(text_buffer, tagged_word_buffer):
    if type(text_buffer) is list:
        text = ''
        for buffer_item in text_buffer:
            text = text + ''.join(
                [w for w in ''.join([l for l in open(buffer_item, "r")]) if is_zh(w)])
    else:
        text = ''.join([w for w in ''.join([l for l in text_buffer]) if is_zh(w)])

    tagged_word = set()
    tot = 0
    for w in tagged_word_buffer:
        w = w[:-1]
        key, weight, tag = w.split(None, 2)
        tagged_word.add(key)
    for t in text:
        if t in tagged_word:
            tot += 1
    print("coverage ratio:%s" % (float(tot)/len(text)))
    return (float(tot)/len(text))

if __name__ == "__main__":
    cnt(open(sys.argv[1], 'r'),
        open(sys.argv[2], 'r'))
