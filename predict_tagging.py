#!/bin/python3
# -*- coding: utf-8 -*-
"""
Scripts for Old Chinese pattern counting.

pattern data saved in JSON format
"""

import json
import re
import os
from collections import defaultdict


PATTERN_FILE = "pattern.json"
TAG_FILE = "tagged.txt"
AUTO_TAG_FILE="auto_tagged.txt"
SENTENCE_FIND_REGEX = re.compile("([^，。？ ]+?)[，。？ ]")
SUB_PUNC_REGEX = re.compile("[「」『』、；\n]")
update_similarity = lambda origin_similarity, new_similarity: \
                           new_similarity if new_similarity[0] > origin_similarity[0] else origin_similarity
is_zh = (lambda x: True if 19968 <= ord(x) <= 40908 else False)


def find_tagable_char(sentence, pattern, word_dict):

    def similarity(s_idx, p_idx, p_cnt, similarity_value, match_result):
        """
        find maximal simiarlity value
        """
        if p_idx >= len(pattern) or s_idx >= len(sentence):
            return [similarity_value, match_result]
        # print ("sen pos", s_idx, "ptn pos", p_idx, "pattern", pattern[p_idx], "char", sentence[s_idx])
        # print (similarity_value, match_result, sentence[s_idx], word_dict[sentence[s_idx]])
        new_similarity_result = [similarity_value, match_result]
        if p_idx < len(pattern):
            #print (sentence[s_idx], pattern[p_idx+p_cnt][0], '!')
            if p_cnt < len(pattern[p_idx]) and (pattern[p_idx][0] in word_dict[sentence[s_idx]].get("tag", [])) or (
		    pattern[p_idx][0] == sentence[s_idx]): # pattern is a specific char
                # print ("match!", p_cnt, match_result, sentence[s_idx])
                if not match_result:
                    match_result = [0]
                temp_similarity_result = similarity(
                    s_idx+1, p_idx, p_cnt+1, similarity_value+1, match_result[:-1]+[match_result[-1]+1])
                new_similarity_result = update_similarity(new_similarity_result, temp_similarity_result)
            # not match, next pattern position, next char
            temp_similarity_result = similarity(
                s_idx+1, p_idx+1, 0, similarity_value, match_result+[0])
            new_similarity_result = update_similarity(new_similarity_result, temp_similarity_result)
            # not match, next pattern position, current char
            temp_similarity_result = similarity(
                s_idx, p_idx+1, 0, similarity_value, match_result+[0])
            new_similarity_result = update_similarity(new_similarity_result, temp_similarity_result)

        # print (s_idx, p_idx, similarity_value, pattern[p_idx], sentence[s_idx], "result", new_similarity_result)
        return new_similarity_result

    # sentence has no similarity with pattern
    if len(sentence) < len(pattern):
        return None
    print ("sentence len:", len(sentence), "pattern len:", len(pattern))
    similarity_result = similarity(0, 0, 0, 0, [])
    return similarity_result


def predict_tagging(text, pattern_list, word_dict, output_file=AUTO_TAG_FILE):
    """
    tagging untagged char in a sentence then output to output_file

    """
    TAGGING_THRESHOLD = 0.3
    sentence_list = [_ for _ in SENTENCE_FIND_REGEX.findall(text) if is_zh(_)]
    tag_dict = defaultdict(list)
    """
    char tagging format
    "<char>": [pos_0, pos_1]
    """
    similar_char_pos_tag = dict()
    """
    char possible tagging count dict format:
    "<char>": { "total": sum(occurrance),
                "pos_0": occurrance_0,
                "pos_1": occurrance_1 ...}
    """
    # count similarity
    for sentence in sentence_list:
        for pattern in pattern_list:
             result = find_tagable_char(sentence, pattern, word_dict)
             print (result, len(pattern), sentence)
             if result and len(sentence) - (result[0]) == 1: # similarity is 1
                 s_idx = 0
                 for p_idx in range(0, len(result[1])): # len(result[1]) == len(pattern)
                     if result[1][p_idx] == 0:
                         ch = sentence[s_idx]
                         if not similar_char_pos_tag.get(ch):
                             similar_char_pos_tag[ch] = defaultdict(int)
                         similar_char_pos_tag[ch]["total"] += 1
                         similar_char_pos_tag[ch][pattern[p_idx][0]] += 1
                         break
                     else:
                         s_idx += result[1][p_idx]

    print (similar_char_pos_tag)

    # determine chars which should be tagged & tag to which pattern
    for ch, pos in similar_char_pos_tag.items():
        for pattern in pos:
            if pattern != "total":
                print (pattern, ch)
                if pos[pattern] / pos["total"] > TAGGING_THRESHOLD:
                    tag_dict[ch].append(pattern)

    print (tag_dict)
    # output tagged dict
    if output_file:
        with open(output_file, "w") as out:
            for char, tag in tag_dict.items():
                out.write("%s %s\n" % (char, ",".join(tag)))

    return tag_dict


def matching_pattern(sentence, pattern, word_dict):
    """
    @return: True if sentence match pattern, else return False
    """
    def dfs_matching(s_idx, p_idx, match_result):
        """
        pattern counting following a greedy method: matching longest words in text
        if we could match one pattern.
        """
        print (s_idx, p_idx, sentence[s_idx], pattern[p_idx][0], match_result)
        if s_idx == len(sentence) - 1 and p_idx == len(pattern) - 1:
            return match_result
        elif s_idx < len(sentence) - 1 and p_idx < len(pattern) - 1 and ((
                pattern[p_idx][0] in word_dict[sentence[s_idx]].get("tag", [])) or (
                pattern[p_idx][0] == sentence[s_idx])):
            # match same tag first
            temp_result = dfs_matching(s_idx+1, p_idx, match_result[:-1]+[match_result[-1]+1])
            if not temp_result: # try to match new tag
                temp_result = dfs_matching(s_idx+1, p_idx+1, match_result+[1])
            return temp_result
        return False

    if len(sentence) < len(pattern):
        return False

    return dfs_matching(0, 0, [1])


def count_pattern(text, pattern_list, word_dict, output_file="pattern_count_result.json"):
    """
    count sentence pattern in text
    """
    pattern_match_result = [{"pattern": pattern, "_example": []} for pattern in pattern_list]

    sentence_list = [_ for _ in SENTENCE_FIND_REGEX.findall(text) if is_zh(_)]
    # count similarity
    for sentence in sentence_list:
        for p_idx in range(0, len(pattern_list)):
            if matching_pattern(sentence, pattern_list[p_idx], word_dict):
                pattern_match_result[p_idx]["_example"].append(sentence)

    if output_file:
        json.dump(pattern_match_result, open(output_file, "w"))

    return pattern_match_result


def load_pattern_list(pattern_file):
    """
    pattern list file format:
    each pattern expressed as JSON per line
    [("<pos_0>", <maximal_occurrance_0>),
     ("<pos_1>", <maximal_occurrance_1>),
    ...]
    """
    return [json.loads(_) for _ in open(pattern_file, "r")]


def load_word_dict(word_tag_file, has_weight=True):
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
            if has_weight:
                key, weight, tag = w.split(None, 2)
                word_dict[key]['weight'] = int(weight)
            else:
                print (w)
                key, tag = w.split(None, 1)
            word_dict[key]['tag'] = tag.replace(' ', '').split(',')

    return word_dict


def main():

    text_files = [ "text/article/" + f for f in os.listdir("text/article/")]
    text = ''
    for _file in text_files:
        text = text + ''.join(
            [w for w in ''.join(
                    [l for l in open(_file, "r")])])
    text = SUB_PUNC_REGEX.sub(" ", text)

    word_dict = load_word_dict("tagged.txt")
    pattern_list = load_pattern_list("pattern.test.json")

    predict_tagging(text, pattern_list, word_dict)
    word_dict.update(load_word_dict(AUTO_TAG_FILE, has_weight=False))

    # we use same pattern list currently as predict procedure
    count_pattern(text, pattern_list, word_dict)


#-----------------------------TEST----------------------------------------

def test_count_pattern():
    text = "孔子之葉也。此亦飛之至也。義之和也。王曰然。王曰善。"
    word_dict = load_word_dict("tagged.txt")
    pattern_list = [[["N", 2], ["之", 1], ["N", 2], ["也", 1]]]
    predict_tagging(text, pattern_list, word_dict)
    word_dict.update(load_word_dict("auto_tagged.txt", has_weight=False))

    pattern_list = [[["N", 2], ["之", 1], ["N", 2], ["也", 1]],
                    [["N", 2], ["V", 1], ["N", 1]]]
    print (count_pattern(text, pattern_list, word_dict))


def test_matching_pattern():
    text = "孔子之葉也。此亦飛之至也。義之和也。"
    word_dict = load_word_dict("tagged.txt")
    pattern_list = [[["N", 2], ["之", 1], ["N", 2], ["也", 1]]]
    predict_tagging(text, pattern_list, word_dict)
    word_dict.update(load_word_dict("auto_tagged.txt", has_weight=False))

    pattern = [["N", 2], ["之", 1], ["N", 2], ["也", 1]]
    print (matching_pattern("孔子之葉也", pattern, word_dict))


def test_predict_tagging():
    text = "孔子之葉也。此亦飛之至也。義之和也。"
    word_dict = load_word_dict("tagged.txt")
    pattern_list = [[["N", 2], ["之", 1], ["N", 2], ["也", 1]]]
    predict_tagging(text, pattern_list, word_dict)


def test_find_tagable_char():
    word_dict = load_word_dict("tagged.txt")
    #pattern = [["N", 2], ["V", 1], ["N", 2], ["于", 1], ["N", 2]]
    #print (find_tagable_char("鄭伯克段于鄢", word_dict, pattern))
    #pattern = [["N", 2], ["AD", 1], ["P", 1], ["V", 1], ["P", 1]]
    #print(find_tagable_char("孔穿無以應焉", word_dict, pattern))
    pattern = [["N", 2], ["之", 1], ["N", 2], ["也", 1]]
    print (find_tagable_char("孔子之葉也", pattern, word_dict))


if __name__ == "__main__":
    # test_find_tagable_char()
    # test_predict_tagging()
    # test_matching_pattern()
    # test_count_pattern()
    main()
    # load_word_dict("auto_tagged.txt", has_weight=False)
