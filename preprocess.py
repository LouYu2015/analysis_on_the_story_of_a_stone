import re

split_mark = "#"
filtered_chars = "『』［］[]〔〕"
split_chars = " …《》，、。？！；：“”‘’'\n\r-=—()（）.【】"

input_file = open("hlm.txt", "r")
output_file = open("preprocessing.txt", "w")


def str_replace(string, str_from, str_to=""):
    return str_to.join(string.split(str_from))


def str_replace_re(string, str_from, str_to=""):
    return re.sub(str_from, str_to, string)


def preprocessing(string):
    string = str_replace_re(string, "正文 第.{1,5}回")

    for char in filtered_chars:
        string = str_replace(string, char)

    for char in split_chars:
        string = str_replace(string, char, split_mark)

    while split_mark + split_mark in string:
        string = str_replace(string, split_mark + split_mark, split_mark)

    return string


def main():
    string = input_file.read()
    output_file.write(preprocessing(string))

if __name__ == "__main__":
    main()
