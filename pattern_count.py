#!/bin/python3
# -*- coding: utf-8 -*-
"""
this module provide methods for counting patterns in text.
"""
import sys
from collections import defaultdict


def pattern_count(text_buffer, word_list_buffer, s_ptn_list):
    """
    @param word_list_buffer: word with tagged mark.
    format: <word> <weight> <tag_1,tag_2...tag_n>
    """
    if type(text_buffer) is list:
        text = ''
        for buffer_item in text_buffer:
            text = text + ''.join(
                [w for w in ''.join(
                        [l for l in open(buffer_item, "r")]
                        )]
                )
    else:
        text = ''.join([w for w in ''.join([l for l in text_buffer])])

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

    tot_ptn_list = []
    output = open("count_result.out", "w")
    for s_ptn in s_ptn_list:
        tot_ptn = defaultdict(int)
        tot_ocr = 0
        for i in range(0, len(text) - len(s_ptn)):
            ptn = text[i:i+len(s_ptn)]
            if all(p in word_list for p in ptn):
                if all(fit_pattern(ptn[j], s_ptn[j])
                       for j in range(0, len(s_ptn))):
                    tot_ptn[ptn] += 1
                    tot_ocr += 1
                    i += len(ptn)
        print("%s total pattern: %s total occurance: %s" % (
                s_ptn, len(tot_ptn), tot_ocr))
        output.write("%s total pattern: %s total occurance: %s\n" % (
                s_ptn, len(tot_ptn), tot_ocr))
        for p in sorted(tot_ptn, key=lambda x: tot_ptn[x], reverse=True)[:100]:
            print(p, tot_ptn[p])
            output.write("%s %s\n" % (p, tot_ptn))
        #for p in sorted(tot_ptn, key=lambda x: tot_ptn[x], reverse=True):
        tot_ptn_list.append(tot_ptn)
    output.close()
    return tot_ptn_list


if __name__ == "__main__":
    pass
    #example
    #ptn_cnt(open(sys.argv[1], "r"), open(sys.argv[2], "r"), [[['N'], '于', ['N']]])
    #ptn_cnt(open(sys.argv[1], "r"), open(sys.argv[2], "r"), [[['N'], ['V', 'A']]])
    #ptn_cnt(open(sys.argv[1], "r"), open(sys.argv[2], "r"), [[['N'], ['V','A'], ['N']]])
