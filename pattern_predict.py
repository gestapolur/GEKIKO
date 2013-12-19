#!/bin/python3
# -*- coding: utf-8 -*-
"""
this module provide pattern predict feature basis on pattern

count result
"""
import sys
from sentense_pattern_cnt import ptn_cnt
from collections import defaultdict

is_zh = (lambda x: True if 19968 <= ord(x) <= 40908 else False)
grammar_type = {'S': ['N'], 'P': ['V','A'], 'O': ['N']}

def ptn_pdt(text_buffer, word_list_buffer, ptn_lst):
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
    word_tag = dict()
    occur = defaultdict(int)
    for sml in similar_lst:
        for i, w in enumerate(list(sml[0])):
            if not w in word_list:
                
                word_tag[w] = grammar_type[ptn_lst[sml[1]][i]]
                occur[w] += 1
    for w in word_tag:
        print (w, word_tag[w], occur[w])


def ptn_grammar_type_cmp(ptn, sub, tagged_word_lst):
    grammar_type_map = lambda x, y: True if (
        x in tagged_word_lst and any(t in grammar_type[ptn[y]] for t in tagged_word_lst[x]['tag'])) else False
    once = False
    for i, w in enumerate(list(sub)):
        if not grammar_type_map(w, i):
            if not once:
                once = True
            else:
                return []
    if once:
        return sub


def ptn_find_similar(text, ptn_lst, tagged_word_lst):
    """
    @return : similar_lst, [<string>,<pattern_index>]
    """
    #print (tagged_word_lst)
    similar_lst = []
    for idx, ptn in enumerate(ptn_lst):
        for i in range(0, len(text)-len(ptn)):
            sub = text[i:i+len(ptn)]
            if not all(x in sub for x in tagged_word_lst) and all(is_zh(x) for x in sub):
                #print (sub)
                t = ptn_grammar_type_cmp(ptn, sub, tagged_word_lst)
                if t:
                    similar_lst.append((t, idx))
    return similar_lst
            
def ptn_predict_grammar_type(similar_lst):
    return []


ptn_pdt(open(sys.argv[1], 'r'),
        open(sys.argv[2], 'r'),
        [['S', 'P', 'O'], ['S', 'P', 'O', 'O']])
