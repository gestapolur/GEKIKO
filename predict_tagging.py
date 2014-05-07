#!/bin/python3
# -*- coding: utf-8 -*-
"""
Scripts for Old Chinese pattern counting.

"""

import json
import re
import os
from collections import defaultdict

# pattern data saved in JSON format
PATTERN_FILE = "pattern.test.json"
TAG_FILE = "tagged.txt"
AUTO_TAG_FILE="auto_tagged.txt"
PATTERN_COUNT_RESULT = "pattern_count_result.json"
SENTENCE_FIND_REGEX = re.compile("([^，。？ ]+?)[，。？ 　]")
SUB_PUNC_REGEX = re.compile("[　「」『』、；\n]")
update_similarity = lambda origin_similarity, new_similarity: \
                           new_similarity if new_similarity and \
                           (new_similarity[0] > origin_similarity[0] or \
                           (new_similarity[0] == origin_similarity[0] and \
                                new_similarity[1] > origin_similarity[1])) else origin_similarity


def find_max_similarity(sentence, pattern, word_dict):

    def similarity(s_idx, p_idx, p_cnt, similarity_value, match_result):
        """
        find maximal simiarlity value

        sum(_ if _ else 1 for _ in match_result) == len(sentence)
        """
        # if we meet a match, we end it, to 
        if p_idx >= len(pattern) - 1 and s_idx == len(sentence):
            print ("result", similarity_value, match_result)
            return [similarity_value, match_result]
        elif p_idx == len(pattern) or s_idx == len(sentence):
            return None

        print ("sen pos", s_idx, "ptn pos", p_idx, "pattern", pattern[p_idx], "char", sentence[s_idx])
        print (similarity_value, match_result, p_cnt, sentence[s_idx], word_dict[sentence[s_idx]])
        new_similarity_result = [similarity_value, match_result]
        #print (sentence[s_idx], pattern[p_idx+p_cnt][0], '!')
        # not exceed maximal tag count
        if p_cnt < pattern[p_idx][1] and \
                ((pattern[p_idx][0] in word_dict[sentence[s_idx]].get("tag", [])) or \
                     (pattern[p_idx][0] == sentence[s_idx])): # pattern is a specific char
            print ("match!", match_result, sentence[s_idx], pattern[p_idx][0], word_dict[sentence[s_idx]].get("tag", []))
            # match, current pattern position, next char
            if pattern[p_idx][0] == sentence[s_idx]: # specific char can't continue
                temp_similarity_result = similarity(
                    s_idx+1, p_idx+1, 0, similarity_value+1,
                    match_result + [(sentence[s_idx], pattern[p_idx][0], 1)])
                    # match_result[:-1]+[[match_result[-1][0], match_result[-1][1]+1]])
            else:
                temp_similarity_result = similarity(
                    s_idx+1, p_idx, p_cnt+1, similarity_value+1,
                    match_result + [(sentence[s_idx], pattern[p_idx][0], 1)])
                    # match_result[:-1]+[[match_result[-1][0], match_result[-1][1]+1]])
            print ("matched result", temp_similarity_result)
            new_similarity_result = update_similarity(new_similarity_result, temp_similarity_result)

        # not match, ignore current tag, next pattern position, next char
        temp_similarity_result = similarity(
            s_idx+1, p_idx+1, 0, similarity_value,
            match_result + [(sentence[s_idx], pattern[p_idx][0], 0)])
        new_similarity_result = update_similarity(new_similarity_result, temp_similarity_result)
        if p_cnt: # not match, current tag were matched, next pattern position, current char
            """
            only if p_cnt, we could switch tag, or some pattern may not be matched at last
            """
            temp_similarity_result = similarity(
                s_idx, p_idx+1, 0, similarity_value, match_result)
            new_similarity_result = update_similarity(new_similarity_result, temp_similarity_result)

        # print (s_idx, p_idx, similarity_value, pattern[p_idx], sentence[s_idx], "result", new_similarity_result)
        return new_similarity_result

    # sentence has no similarity with pattern
    if len(sentence) < len(pattern) or len(sentence) > sum([_[1] for _ in pattern]):
        return None
    print ("sentence len:", len(sentence), "pattern len:", len(pattern))
    similarity_result = similarity(0, 0, 0, 0, [])
    return similarity_result


def predict_tagging(text, pattern_list, word_dict, output_file=AUTO_TAG_FILE):
    """
    tagging untagged char in a sentence then output to output_file

    """
    TAGGING_THRESHOLD = 0.3
    sentence_list = SENTENCE_FIND_REGEX.findall(text)
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
             result = find_max_similarity(sentence, pattern, word_dict)
             print (result, len(pattern), pattern, sentence)
             if result and (len(sentence) - result[0] == 1): # similarity is 1
                 assert len(result[1]) == len(sentence)
                 for char, tag, is_tagged in result[1]:
                     if not is_tagged:
                         if not similar_char_pos_tag.get(char):
                             similar_char_pos_tag[char] = defaultdict(int)
                         similar_char_pos_tag[char]["total"] += 1
                         similar_char_pos_tag[char][tag] += 1
                         break

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

    if len(sentence) < len(pattern) or len(sentence) > sum([_[1] for _ in pattern]):
        return False

    return dfs_matching(0, 0, [1])


def count_pattern(text, pattern_list, word_dict, output_file=PATTERN_COUNT_RESULT):
    """
    count sentence pattern in text
    """
    pattern_match_result = [{"pattern": pattern, "_example": []} for pattern in pattern_list]

    sentence_list = SENTENCE_FIND_REGEX.findall(text)
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


def load_corpus():
    text_files = [ "text/article/" + f for f in os.listdir("text/article/")]
    text = ''
    for _file in text_files:
        text = text + ''.join(
            [w for w in ''.join(
                    [l for l in open(_file, "r")])])
    return SUB_PUNC_REGEX.sub(" ", text)


def main():
    text = load_corpus()

    word_dict = load_word_dict(TAG_FILE)
    pattern_list = load_pattern_list(PATTERN_FILE)

    predict_tagging(text, pattern_list, word_dict)
    word_dict.update(load_word_dict(AUTO_TAG_FILE, has_weight=False))

    # we use same pattern list currently as predict procedure
    count_pattern(text, pattern_list, word_dict)

#-----------------------------TEST----------------------------------------

def test_count_pattern():
    text = "孔子之葉也。此亦飛之至也。義之和也。王曰然。王曰善。百姓親。"
    word_dict = load_word_dict("tagged.txt")
    pattern_list = [[["N", 2], ["之", 1], ["N", 2], ["也", 1]]]
    predict_tagging(text, pattern_list, word_dict, output_file="auto_tagged.test.txt")
    word_dict.update(load_word_dict("auto_tagged.test.txt", has_weight=False))

    pattern_list = [[["N", 2], ["之", 1], ["N", 2], ["也", 1]],
                    [["N", 2], ["V", 1], ["N", 1]]]
    print (count_pattern(text, pattern_list, word_dict))


def test_matching_pattern():
    text = "孔子之葉也。此亦飛之至也。義之和也。"
    word_dict = load_word_dict("tagged.txt")
    pattern_list = [[["N", 2], ["之", 1], ["N", 2], ["也", 1]]]
    predict_tagging(text, pattern_list, word_dict, output_file="auto_tagged.test.txt")
    word_dict.update(load_word_dict("auto_tagged.test.txt", has_weight=False))

    pattern = [["N", 2], ["之", 1], ["N", 2], ["也", 1]]
    print (matching_pattern("孔子之葉也", pattern, word_dict))

    pattern = [["N", 2], ["V", 1], ["N", 2]]
    print (word_dict["百"], word_dict["姓"], word_dict["親"])
    print (matching_pattern("百姓親", pattern, word_dict))


def test_predict_tagging():
    text = "孔子之葉也。此亦飛之至也。義之和也。梁惠王。"
    word_dict = load_word_dict("tagged.txt")
    pattern_list = [[["N", 2], ["之", 1], ["N", 2], ["也", 1]],
                    [['A', 1], ['于', 1], ['N', 2]]]
    predict_tagging(text, pattern_list, word_dict, output_file="auto_tagged.test.txt")


def test_find_max_similarity():
    word_dict = load_word_dict("tagged.txt")

    pattern = [["N", 2], ["V", 1], ["N", 2], ["于", 1], ["N", 2]]
    assert (
        find_max_similarity("鄭伯克段于鄢", pattern, word_dict) == \
            [4, [('鄭', 'N', 1), ('伯', 'N', 1), ('克', 'V', 1), ('段', 'N', 0), ('于', '于', 1), ('鄢', 'N', 0)]])

    pattern = [["N", 2], ["AD", 1], ["PR", 1], ["V", 1], ["P", 1]]
    assert (
        find_max_similarity("孔穿無以應焉", pattern, word_dict) == \
            [4,
             [('孔', 'N', 1), ('穿', 'N', 0), ('無', 'AD', 1), ('以', 'PR', 1), ('應', 'V', 0), ('焉', 'P', 1)]])

    pattern = [["N", 2], ["之", 1], ["N", 2], ["也", 1]]
    assert (find_max_similarity(
            "孔子之葉也", pattern, word_dict) == \
               [4, [('孔', 'N', 1), ('子', 'N', 1), ('之', '之', 1), ('葉', 'N', 0), ('也', '也', 1)]])

    pattern = [['A', 1], ['于', 1], ['N', 2]]
    assert (find_max_similarity(
            "梁惠王", pattern, word_dict) == [1, [('梁', 'A', 0), ('惠', '于', 0), ('王', 'N', 1)]])

    pattern = [['N', 2], ['V', 1], ['于', 1], ['N', 2]]
    assert (find_max_similarity("故能樂也", pattern, word_dict) ==\
                [2, [('故', 'N', 1), ('能', 'V', 1), ('樂', '于', 0), ('也', 'N', 0)]])


if __name__ == "__main__":
    # test_find_max_similarity()
    # test_predict_tagging()
    # test_matching_pattern()
    # test_count_pattern()
    main()
