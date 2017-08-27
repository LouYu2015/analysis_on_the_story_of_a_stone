import suffix_tree
import math

split_mark = "#"

friendly_split_mark = "，"
word_split_mark = "/"

input_file = open("preprocessing.txt", "r")
dict_file = open("dict.csv", "r")

decay = 1000


def load():
    return input_file.read()


def construct_tree(string):
    tree = suffix_tree.SuffixTree(string)
    tree.update_counter()
    return tree


def load_dict():
    dictionary = dict()
    lines = dict_file.read().split("\n")
    count_sum = 0
    for line in lines:
        if line:
            cols = line.split(",")
            dictionary[cols[0]] = int(cols[1])*float(cols[-1])
            count_sum += int(cols[1])
    return {key: value/count_sum for key, value in dictionary.items()}


def count_sentence_length(string):
    sentences = string.split(split_mark)
    length = [len(string) for string in sentences]
    max_length = max(length)

    count = [0]*(max_length+1)
    for l in length:
        count[l] += 1

    return count


def count_all_possibilities(sentence_length_count, word_length):
    count_sum = 0
    for length, count in enumerate(sentence_length_count):
        if length >= word_length:
            count_sum += count*(length - word_length + 1)
    return count_sum


def get_prob(tree, dictionary, sentence_length_count, string):
    global decay
    try:
        current_word_prob = dictionary[string]
    except KeyError:
        current_word_count = tree.query(string).counter
        current_word_prob = current_word_count / count_all_possibilities(sentence_length_count, len(string))

        if current_word_count == 1:
            for i in range(len(string)-1):
                current_word_prob /= decay

    return current_word_prob


def split(tree, dictionary, sentence_length_count, string):
    prob = [1]
    last_word_index = [0]

    for i in range(1, len(string)+1):
        max_prob = -1
        max_prob_candidate = None
        have_whole_word = False
        for candidate in range(max(0, i-4), i):
            # last_word = string[last_word_index[candidate]: candidate]
            current_word = string[candidate: i]
            current_prob = prob[candidate]*get_prob(tree, dictionary, sentence_length_count, current_word)

            if current_prob > max_prob:
                max_prob = current_prob
                max_prob_candidate = candidate

            # print("[%d:%d]%s/%s:%.10f" % (candidate, i, last_word, current_word, current_prob))

        prob.append(max_prob)
        last_word_index.append(max_prob_candidate)

    result = []
    cursor = len(string)
    while cursor != 0:
        prev = last_word_index[cursor]
        result.append(string[prev: cursor])
        cursor = prev
    return list(reversed(result))


def split2(tree, dictionary, sentence_length_count, string):
    max_prob = get_prob(tree, dictionary, sentence_length_count, string)
    result = string

    for i in range(1, len(string)):
        prob_left, result_left = split2(tree, dictionary, sentence_length_count, string[:i])
        prob_right, result_right = split2(tree, dictionary, sentence_length_count, string[i:])

        if prob_left*prob_right > max_prob:
            result = result_left + word_split_mark + result_right
            max_prob = prob_left*prob_right

    # print(string, max_prob, result)
    return max_prob, result


def split_all(tree, dictionary, sentence_length_count, string, out_file):
    all_list = string.split(split_mark)
    for i, s in enumerate(all_list):
        out_file.write(word_split_mark.join(split(tree, dictionary, sentence_length_count, s)))
        out_file.write(friendly_split_mark)

        if i % 100 == 0:
            print(i/len(all_list))

    out_file.write("\n\n")


def main():
    print("Loading dictionary")
    dictionary = load_dict()

    print("Building tree")
    string = load()
    tree = construct_tree(string)
    sentence_length_count = count_sentence_length(string)

    print("Processing")
    output_file = open("word_split.txt", "w")
    global decay
    decay = 1000

    split_all(tree, dictionary, sentence_length_count, string, output_file)


def test_cursor():
    tree = construct_tree("banana$")
    tree.root.visualize()
    cursor = tree.query_cursor("an")
    cursor.node.visualize()
    cursor.current_node.visualize()
    cursor.move_front_forward()
    cursor.node.visualize()
    cursor.current_node.visualize()


if __name__ == "__main__":
    # test_cursor()
    main()