#bin/python3
import os
import sys
from pattern_predict import read_pattern
from pattern_predict import pattern_predict
from pattern_count import pattern_count
from coverage import cnt

text_files = [ "text/article/" + f for f in os.listdir("text/article/")]
"""
pattern_count(
    text_files,
    open("tagged.txt", "r"),
    read_pattern(open(sys.argv[1], "r"))
    )
"""
pattern_count(
    text_files,
    open("test_tag.txt", "r"),
    read_pattern(open(sys.argv[1], "r"))
    )

exit(0)

pattern_predict(
    text_files,
    open("tagged.txt", "r"),
    read_pattern(open(sys.argv[1], "r"))
    )

print ("before POS coverage rate\n ====")
c1 = cnt(text_files,
    open("tagged.txt", "r")
    )

print ("POS coverage rate\n ====\n")
c2 = cnt(text_files,
    open("predicted_pattern.txt", "r")
    )

print ("Total coverage rate: %s" % (c1 + c2))
