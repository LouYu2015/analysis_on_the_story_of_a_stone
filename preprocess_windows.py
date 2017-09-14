"""
Author: Yu Lou
"""
import re

split_mark = "#"  # Split mark for output
filtered_chars = "『』［］[]〔〕"  # Characters to ignore
split_chars = " …《》，、。？！；：“”‘’'\n\r-=—()（）.【】"  # Characters representing split mark

input_file = open("hlm_ANSI.txt", "r", encoding="gbk", errors="ignore")  # Open input file


def str_replace(string, str_from, str_to=""):
    """
    Replace str_from with str_to in string.
    """
    return str_to.join(string.split(str_from))


def str_replace_re(string, str_from, str_to=""):
    """
    Replace str_from with str_to in string.
    str_from can be an re-expression.
    """
    return re.sub(str_from, str_to, string)


def preprocessing(string):
    """
    Preprocess string.
    :return: processed string
    """
    string = str_replace_re(string, "正文 第.{1,5}回")

    for char in filtered_chars:
        string = str_replace(string, char)

    for char in split_chars:
        string = str_replace(string, char, split_mark)

    # Remove consecutive split marks
    while split_mark + split_mark in string:
        string = str_replace(string, split_mark + split_mark, split_mark)

    return string


def main():
    output_file = open("preprocessing.txt", "w")

    string = input_file.read()
    output_file.write(preprocessing(string))

if __name__ == "__main__":
    main()
