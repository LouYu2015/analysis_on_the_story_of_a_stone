import suffix_tree
import math

split_mark = "#"

friendly_split_mark = "，"
word_split_mark = "/"

input_file = open("preprocessing.txt", "r")
output_file = open("word_split.txt", "w")


def load():
    return input_file.read()


def construct_tree(string):
    tree = suffix_tree.SuffixTree(string)
    tree.update_counter()
    return tree


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


def split(tree, sentence_length_count, string):
    prob = [1]
    last_word_index = [0]

    for i in range(1, len(string)+1):
        max_prob = -1
        max_prob_candidate = None
        for candidate in range(max(0, i-5), i):
            last_word = string[last_word_index[candidate]: candidate]
            current_word = string[candidate: i]

            if last_word:
                current_word_count = tree.query(current_word).counter
                last_word_count = tree.query(last_word).counter
                all_count = tree.query(last_word + current_word).counter

                current_word_prob = current_word_count/count_all_possibilities(sentence_length_count, len(current_word))
                last_word_prob = last_word_count/count_all_possibilities(sentence_length_count, len(last_word))
                all_prob = all_count/count_all_possibilities(sentence_length_count, len(last_word + current_word))

                current_prob = current_word_prob*last_word_prob/all_prob

                # print(current_prob, last_word_prob)
            else:
                current_word_count = tree.query(split_mark+current_word).counter
                all_possibilities = tree.query(split_mark).counter
                # all_possibilities = current_word_count/count_all_possibilities(sentence_length_count, len(current_word))
                # all_possibilities = sum(sentence_length_count)
                current_prob = current_word_count/all_possibilities

                # print(current_word_count, all_possibilities)

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


def split_all(tree, sentence_length_count, string):
    result = []
    for s in string[:10000].split(split_mark):
        result.append(word_split_mark.join(split(tree, sentence_length_count, s)))
    return friendly_split_mark.join(result)


def main():
    string = load()
    tree = construct_tree(string)
    sentence_length_count = count_sentence_length(string)
    result = split_all(tree, sentence_length_count, string)
    output_file.write(result)


if __name__ == "__main__":
    main()
