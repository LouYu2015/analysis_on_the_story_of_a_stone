word_split_marks = "/\n"  # Split marks for word
split_mark = "，"  # Split marks for sentence

file_name = input("Enter file prefix:")

input_file = open("%s_result.txt" % file_name, "r")
answer = open("%s_answer.txt" % file_name, "r")


def split_all(string):
    ''.join(string.split(split_mark))

    for word_split_mark in word_split_marks:
        string = word_split_marks[0].join(string.split(word_split_mark))
    result = string.split(word_split_marks[0])
    return [word for word in result if word]

result = split_all(input_file.read())
answer = split_all(answer.read())

assert "".join(result) == "".join(answer), "Content is not the same"

len_result = 0
len_answer = 0
cursor_result = 0
cursor_answer = 0

true_positive = -1
false_positive = 0
false_negative = 0

while cursor_result != len(result) and cursor_answer != len(answer):
    if len_result == len_answer:
        true_positive += 1

        len_result += len(result[cursor_result])
        cursor_result += 1

        len_answer += len(answer[cursor_answer])
        cursor_answer += 1

    elif len_result < len_answer:
        false_positive += 1

        len_result += len(result[cursor_result])
        cursor_result += 1

    elif len_result > len_answer:
        false_negative += 1

        len_answer += len(answer[cursor_answer])
        cursor_answer += 1

    # print(len_result, len_answer)
    # print(cursor_result, cursor_answer)
    # print()


precision = true_positive/(true_positive + false_positive)
recall = true_positive/(true_positive + false_negative)
f1 = 2/(1/precision + 1/recall)

print("True positive:", true_positive)
print("False positive:", false_positive)
print("False negative:", false_negative)
print("Precision: %.2f%%" % (precision*100))
print("Recall: %.2f%%" % (recall*100))
print("F1: %.2f%%" % (f1*100))
