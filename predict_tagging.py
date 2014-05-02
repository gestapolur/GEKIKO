#!/bin/python3
# -*- coding: utf-8 -*-
"""
this module provide pattern predict feature which base on pattern

count results.

pattern data saved in JSON format
"""

import json
import re
from collections import defaultdict

def similarity(sentence, word_dict, pattern):

    def similarity_match(s_idx, p_idx, similarity_value, match_result):
        """
        find maximal simiarlity value
        """
        if p_idx == len(pattern):
            return similarity_value
        new_similarity_value = similarity_value
        for p_cnt in range(0, pattern[p_idx][2]+1):
            if p_idx+p_cnt < len(pattern)
                if pattern[p_idx+p_cnt] in word_dict[sentense[s_idx]]:
                    new_similarity_value = max(
                        similarity_match(
                            s_idx+p_cnt+1, p_idx+1, similarity_value, match_result+p_cnt),
                        new_similarity_value) + 1
                else: # not match
                    new_similarity_value = max(
                        similarity_match(
                            s_idx+p_cnt+1, p_idx+1, similarity_value, match_result+p_cnt),
                        new_similarity_value)
                
        return new_similarity_value

    # sentence has no similarity with pattern
    if len(sentence) < len(pattern):
        return None
    return similarity_match(0, 0, 0, [])


def predict_tagging(text, word_dict, pattern_list):
    """
    tagging untagged char in a sentence
    """
    SENTENCE_FIND_REGEX = re.compile("(.+?)[，。]")
    sentence_list = SENTENCE_FIND_REGEX.findall(text)
    tagged_dict = {}
    pos_similar_chars = defaultdict(int)
    """
    dict format:
    "<char>": { "total": sum(occurrance),
                "pos_0": occurrance_0,
                "pos_1": occurrance_1 ...}
    """
    # count all not tagged chars

    # count similarity
    for sentence in sentence_list:
        for pattern in pattern_list:
             result = similarity(sentence, word_dict, pattern)
             if type(result) is tuple:
                 pos_similar_chars[result[0]]["total"] += 1
                 pos_similar_chars[result[0]][result[1]] += 1

    # determine chars which should be tagged

    # output tagged dict
    #with open("auto_tagged.txt", "w") as out:
    #    for word in tagged_dict:
    #        out.write("%s %s\n" % (word, tagged_dict[word]))


def load_pattern_list(pattern_file):
    """
    pattern list file format:
    each pattern expressed as JSON per line
    [("<pos_0>", <maximal_occurrance_0>),
     ("<pos_1>", <maximal_occurrance_1>),
    ...]
    """
    return [json.loads(_) for _ in open(pattern_file, "r")]


def load_word_dict(word_tag_file):
    """
    word tagging file format:
    <word> <occurrance> <[POS_0,POS_1...]>
    example: 輿 58 C,N,V,A

    @return: dict, char -> {"tag": [POS_list], "weight": occurrance}
    """
    word_dict = defaultdict(dict)
    with open(word_tag_file, "r") as word_tags:
        for w in word_tags:
            w = w[:-1]
            key, weight, tag = w.split(None, 2)
            word_dict[key]['tag'] = tag.replace(' ', '').split(',')
            word_dict[key]['weight'] = int(weight)

    return word_dict


if __name__ == "__main__":
    # load_word_dict("tagged.txt")
    # pattern_list = load_pattern_list("pattern.test.json")
    # print (type(pattern_list), pattern_list)
