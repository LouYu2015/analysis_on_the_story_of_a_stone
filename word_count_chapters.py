import os
import math

word_split_mark = "/"
split_mark = "，"

number_of_chapters = 120
input_folder = "chapters_split"


def variance(array):
    """
    Calculate variance of a list of numbers.
    """
    mean = sum(array)/len(array)

    result = 0
    for number in array:
        result += abs(number - mean)**2
    return math.sqrt(result/len(array))


def count_word_for_chapter(counter, chapter_no, words):
    for word in words:
        if len(word) <= 1:
            continue

        if word in counter:
            counter[word][chapter_no-1] += 1
        else:
            counter[word] = [0]*number_of_chapters
            counter[word][chapter_no-1] = 1


def count_all_chapter():
    counter = dict()

    for chapter_no in range(1, number_of_chapters + 1):
        input_file = open(os.path.join(input_folder, "%d.txt" % chapter_no), "r")
        string = input_file.read()
        string = ''.join(string.split("\n"))

        string = word_split_mark.join(string.split(split_mark))
        words = string.split(word_split_mark)

        count_word_for_chapter(counter, chapter_no, words)

    return counter


def save_data(counter, output_file):
    table = list(counter.items())
    table.sort(key=lambda x: sum(x[1]), reverse=True)

    for row in table:
        if len(row[0]) > 1:
            output_file.write(row[0] + ",")
            for number in row[1]:
                output_file.write("%d," % number)

            row_variance = variance(row[1])
            output_file.write("%d,%f,%f\n" % (sum(row[1]), row_variance, row_variance/sum(row[1])))


def main():
    output_file = open("word_count_chapters.csv", "w")
    counter = count_all_chapter()
    save_data(counter, output_file)

if __name__ == "__main__":
    main()
