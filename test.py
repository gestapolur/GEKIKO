#bin/python3
import os
from pattern_predict import read_pattern
from pattern_predict import pattern_predict


text_files = [ "text/article/" + f for f in os.listdir("text/article/")]

pattern_predict(
    text_files,
    open("tagged.txt", "r"),
    read_pattern(open("pattern.in", "r"))
    )
