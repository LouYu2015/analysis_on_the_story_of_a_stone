import word_split
import dict_creat
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
    sentence_length_count = dict_creat.count_sentence_length(string)

    print("Processing")
    progress_update_interval = number_of_chapters//20
    for chapter_no in range(1, number_of_chapters+1):
        if chapter_no % progress_update_interval == 1:
            print("|", end="", flush=True)

        input_file = open(os.path.join(chapter_folder, "%d.txt" % chapter_no), "r")
        output_file = open(os.path.join(result_folder, "%d.txt"% chapter_no), "w")
        string = input_file.read()
        word_split.split_all(tree, dictionary, sentence_length_count, string, output_file, show_progress=False)
    print()


if __name__ == '__main__':
    main()
