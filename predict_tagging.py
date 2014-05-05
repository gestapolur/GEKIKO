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

update_similarity = lambda origin_similarity, new_similarity: new_similarity if new_similarity[0] > origin_similarity[0] else origin_similarity

def find_tagable_char(sentence, word_dict, pattern):

    def similarity(s_idx, p_idx, p_cnt, similarity_value, match_result):
        """
        find maximal simiarlity value
        """
        if p_idx >= len(pattern) or s_idx >= len(sentence):
            return [similarity_value, match_result]
        print (s_idx, "current pattern position", p_idx, "pattern name", pattern[p_idx])
        print (s_idx, p_idx, similarity_value, match_result, sentence[s_idx], word_dict[sentence[s_idx]])
        new_similarity_result = [similarity_value, match_result]
        if p_idx < len(pattern):
            #print (sentence[s_idx], pattern[p_idx+p_cnt][0], '!')
            if p_cnt < len(pattern[p_idx]) and (pattern[p_idx][0] in word_dict[sentence[s_idx]].get("tag", [])) or (
		    pattern[p_idx][0] == sentence[s_idx]): # pattern is a specific char
                print (p_cnt, match_result, sentence[s_idx])
                if not match_result:
                    match_result = [0]
                temp_similarity_result = similarity(
                    s_idx+1, p_idx, p_cnt+1, similarity_value+1, match_result[:-1]+[match_result[-1]+1])
                new_similarity_result = update_similarity(new_similarity_result, temp_similarity_result)
            # not match, stay blank on this position
            temp_similarity_result = similarity(
                s_idx+1, p_idx+1, 0, similarity_value, match_result+[0])
        new_similarity_result = update_similarity(new_similarity_result, temp_similarity_result)
        return new_similarity_result

    # sentence has no similarity with pattern
    if len(sentence) < len(pattern):
        return None
    print ("sentence len:", len(sentence), "pattern len:", len(pattern))
    similarity_result = similarity(0, 0, 0, 0, [])
    return similarity_result


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
             result = find_tagable_char(sentence, word_dict, pattern)
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


def test_find_tagable_char():
    word_dict = load_word_dict("tagged.txt")
    #pattern = [["N", 2], ["V", 1], ["N", 2], ["于", 1], ["N", 2]]
    #print (find_tagable_char("鄭伯克段于鄢", word_dict, pattern))
    #pattern = [["N", 2], ["AD", 1], ["P", 1], ["V", 1], ["P", 1]]
    #print(find_tagable_char("孔穿無以應焉", word_dict, pattern))
    pattern = [["N", 2], ["之", 1], ["N", 2], ["也", 1]]
    print (find_tagable_char("孔子之葉也", word_dict, pattern))


if __name__ == "__main__":
    test_find_tagable_char()
    # load_word_dict("tagged.txt")
    # pattern_list = load_pattern_list("pattern.test.json")
    # print (type(pattern_list), pattern_list)
