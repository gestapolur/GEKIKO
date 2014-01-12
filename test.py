#bin/python3
import os
import sys
from pattern_predict import read_pattern
from pattern_predict import pattern_predict


text_files = [ "text/article/" + f for f in os.listdir("text/article/")]

pattern_predict(
    text_files,
    open("tagged.txt", "r"),
    read_pattern(open(sys.argv[1], "r"))
    )
