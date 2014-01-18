#!/bin/python3
# -*- coding: utf-8 -*-
"""
this module provide methods for counting patterns in text.
"""
import sys
from collections import defaultdict
from grammar import is_zh


def ptn_cnt(text_buffer, word_list_buffer, s_ptn):
    """
    @param word_list_buffer: word with tagged mark.
    format: <word> <weight> <tag_1,tag_2...tag_n>
    """
    #text = ''.join([w for w in ''.join([l for l in text_buffer]) if is_zh(w)])
    if not isinstance(text_buffer, str):
        text = ''.join([w for w in ''.join([l for l in text_buffer])])
    else:
        text = text_buffer
    word_list = defaultdict(dict)
    if isinstance(word_list_buffer, defaultdict):
        word_list = word_list_buffer
    else:
        for w in word_list_buffer:
            w = w[:-1]
            key, weight, tag = w.split(None, 2)
            word_list[key]['tag'] = tag.replace(' ', '').split(',')
            word_list[key]['weight'] = int(weight)
    """
    pattern x could fit on position y
    """
    fit_pattern = lambda x, y: True if (
        any(tag in y for tag in word_list[x]['tag'])
        ) or (x == y) else False

    tot_ptn = defaultdict(int)
    for i in range(0, len(text) - len(s_ptn)):
        ptn = text[i:i+len(s_ptn)]
        if all(p in word_list for p in ptn):
            if all(fit_pattern(ptn[j], s_ptn[j])
                   for j in range(0, len(s_ptn))):
                tot_ptn[ptn] += 1
                i += len(ptn)
    print("total occurrence: ", len(tot_ptn))
    for p in sorted(tot_ptn, key=lambda x: tot_ptn[x], reverse=True)[:10]:
        print(p, tot_ptn[p])
    return tot_ptn


if __name__ == "__main__":
    #example
    ptn_cnt(open(sys.argv[1], "r"), open(sys.argv[2], "r"), [['N'], '于', ['N']])
    ptn_cnt(open(sys.argv[1], "r"), open(sys.argv[2], "r"), [['N'], ['V', 'A']])
    ptn_cnt(open(sys.argv[1], "r"), open(sys.argv[2], "r"), [['N'], ['V','A'], ['N']])
