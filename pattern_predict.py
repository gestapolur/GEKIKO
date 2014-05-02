#!/bin/python3
# -*- coding: utf-8 -*-
"""
this module provide pattern predict feature which base on pattern

count results.
"""
import sys
from collections import defaultdict
from grammar import is_zh
from pprint import pprint


def pattern_predict(text_buffer, word_list_buffer, ptn_lst):
    """
    return tagged words & type
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
    for w in word_list_buffer:
        w = w[:-1]
        key, weight, tag = w.split(None, 2)
        word_list[key]['tag'] = tag.replace(' ', '').split(',')
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
        print(sml)
        for i, w in enumerate(list(sml[0])):
            # not tagged before and not a known char in pattern
            if not (w in word_list) and isinstance(ptn_lst[sml[1]][i], list):
                if '_example' in word_tag[w] and \
                        (any(sml[0] in s for s in word_tag[w].get('_example'))):
                    continue
                #print (ptn_lst[sml[1]][i], w)
                for word_type in ptn_lst[sml[1]][i]:
                    word_tag[w][word_type] = inc(word_tag[w], word_type)
                try:
                    word_tag[w]['_example'].append(sml[0])
                except KeyError:
                    word_tag[w]['_example'] = [sml[0]]

    # POS frequency filter, remove POS below average occurance.
    for w, tags in word_tag.items():
        total_cnt = len(tags) - 1
        if total_cnt:
            total_cnt = float(total_cnt)
            average_occur = \
                sum([tags[w] for w in iter(tags) if not(w == '_example')]) / total_cnt
            low_rate_ptn = []
            for tag, cnt in tags.items():
                if not(tag == '_example') and (cnt < average_occur):
                    low_rate_ptn.append(tag)
            for ptn in low_rate_ptn:
                tags.pop(ptn)

    output = open("predicted_tag.txt", "w")
    output_with_example = open("predicted_pattern.txt", "w")
    for w in word_tag:
        #pprint([{k: word_tag[w][k]} for k in sorted(word_tag[w])])
        output.write("%s %s %s\n" % (
                w,
                len(word_tag[w]) - 1,
                str([k for k in sorted(word_tag[w]) if k != "_example"])
                ))
        output_with_example.write("%s %s\n" % (
                w,
                str([{k: word_tag[w][k]} for k in sorted(word_tag[w])])
                ))

    output.close()
    output_with_example.close()


def ptn_grammar_type_cmp(ptn, sub, tagged_word_lst):
    grammar_type_map = lambda x, y: True if (
        any(t in y for t in tagged_word_lst[x]['tag']
            )) or (x == y) else False
    once = False
    for i, w in enumerate(list(sub)):
        if w in tagged_word_lst:
            if not grammar_type_map(w, ptn[i]):
                return False # sub not belong to this pattern
        else:
            if not once:
                once = True
            else: # ensure pattern & sub has exactly 1 differ
                return False
    return once


def ptn_find_similar(text, ptn_lst, tagged_word_lst):
    """
    find sub-sequence which has exactly 1 difference with a pattern.

    @return : similar_lst, [<string>, <pattern_index>]
    """
    similar_lst = []
    for idx, ptn in enumerate(ptn_lst):
        for i in range(0, len(text)-len(ptn)):
            sub = text[i:i+len(ptn)]
            #print(sub, ptn, len(ptn))
            if not all(x in sub for x in tagged_word_lst)and all(is_zh(x) for x in sub):
                if ptn_grammar_type_cmp(ptn, sub, tagged_word_lst):
                    similar_lst.append((sub, idx))
    return similar_lst

def read_pattern(pattern_buffer):
    # python2.x may meet decode problem
    # de = lambda l: [x if isinstance(x, list) else x.encode('latin-1').decode('utf-8') for x in l]
    return [eval(p) for p in pattern_buffer]


if __name__ == "__main__":
    # sample usage
    #pattern_predict(open(sys.argv[1], 'r'),
    #        open(sys.argv[2], 'r'),
    #        [[['N'], ['V','A'], ['N']],
    #         [['N'], ['V','A'], ['N'], ['N']],
    #         [['N'], ['N'], ['V'], ['N']],
    #         [['V'], '于', ['N']],
    #         [['N'], ['V'], '於', ['N']],
    #         ['非', ['N'], ['N'], '也']
    #         ])
    #print(read_pattern(open(sys.argv[1], 'r')))
    pattern_predict(open(sys.argv[1], 'r'),
                    open(sys.argv[2], 'r'),
                    read_pattern(open(sys.argv[3], 'r')))
