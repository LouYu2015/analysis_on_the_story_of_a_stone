import preprocess
import os

chapter_folder = "chapters"
chapter_split_mark = "$"


def main():
    if not os.path.exists(chapter_folder):
        os.makedirs(chapter_folder)

    string = preprocess.input_file.read()
    string = preprocess.str_replace_re(string, "正文 第.{1,5}回", chapter_split_mark)
    for chapter_no, chapter_string in enumerate(string.split(chapter_split_mark)):
        file_name = os.path.join(chapter_folder, "%d.txt" % chapter_no)
        chapter_file = open(file_name, "w")
        chapter_file.write(preprocess.preprocessing(chapter_string))

if __name__ == '__main__':
    main()
