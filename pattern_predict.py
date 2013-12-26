#!/bin/python3
# -*- coding: utf-8 -*-
"""
this module provide pattern predict feature basis on pattern

count result
"""
import sys
from sentense_pattern_cnt import ptn_cnt
from collections import defaultdict
from grammar import is_zh
from grammar import grammar_type

def pattern_predict(text_buffer, word_list_buffer, ptn_lst):
    """
    return tagged words & type
    """
    text = ''.join([w for w in ''.join([l for l in text_buffer])])
    word_list = defaultdict(dict)    
    for w in word_list_buffer:
        w = w[:-1]
        key, weight, tag = w.split(' ')
        word_list[key]['tag'] = tag.split(',')
        word_list[key]['weight'] = int(weight)

    similar_lst = ptn_find_similar(text, ptn_lst, word_list)

    # tag char
    word_tag = defaultdict(dict)
    """
    word tag:{
    "N": 1,
    "V": 2,
    "example": []
    }
    """
    inc = lambda d, k: d[k] + 1 if k in d else 1
    for sml in similar_lst:
        for i, w in enumerate(list(sml[0])):
            if not (w in word_list): # not tagged before
                for word_type in grammar_type[ptn_lst[sml[1]][i]]:
                    word_tag[w][word_type] = inc(word_tag[w], word_type)
                try:
                    word_tag[w]['example'].append(sml[0])
                except KeyError:
                    word_tag[w]['example'] = [sml[0]]
    for w in word_tag:
        print (w, word_tag[w])


def ptn_grammar_type_cmp(ptn, sub, tagged_word_lst):
    grammar_type_map = lambda x, y: True if any(
        t in grammar_type[ptn[y]] for t in tagged_word_lst[x]['tag']
        ) else False
    once = False
    for i, w in enumerate(list(sub)):
        if w in tagged_word_lst:
            if not grammar_type_map(w, i):
                return False # sub not belong to this pattern
        else:
            if not once:
                once = True
            else: # ensure pattern & sub has exactly 1 differ
                return False
    return once


def ptn_find_similar(text, ptn_lst, tagged_word_lst):
    """
    @return : similar_lst, [<string>, <pattern_index>]
    """
    similar_lst = []
    for idx, ptn in enumerate(ptn_lst):
        for i in range(0, len(text)-len(ptn)):
            sub = text[i:i+len(ptn)]
            if not all(x in sub for x in tagged_word_lst)and all(is_zh(x) for x in sub):
                if ptn_grammar_type_cmp(ptn, sub, tagged_word_lst):
                    similar_lst.append((sub, idx))
    return similar_lst


pattern_predict(open(sys.argv[1], 'r'),
        open(sys.argv[2], 'r'),
        [['S', 'P', 'O'],
         ['S', 'P', 'O', 'O'],
         ['S', 'S', 'P', 'O']
         ])
