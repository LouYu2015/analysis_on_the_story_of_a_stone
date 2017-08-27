import word_split
import os

chapter_folder = "chapters"
result_folder = "chapters_split"
number_of_chapters = 120


def main():
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    print("Loading dictionary")
    dictionary = word_split.load_dict()

    print("Building tree")
    string = word_split.load()
    tree = word_split.construct_tree(string)
    sentence_length_count = word_split.count_sentence_length(string)

    print("Processing")
    global decay
    decay = 1000

    for chapter_no in range(1, number_of_chapters+1):
        input_file = open(os.path.join(chapter_folder, "%d.txt" % chapter_no), "r")
        output_file = open(os.path.join(result_folder, "%d.txt"% chapter_no), "w")
        string = input_file.read()
        word_split.split_all(tree, dictionary, sentence_length_count, string, output_file)

if __name__ == '__main__':
    main()