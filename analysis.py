import word_count_chapters

from sklearn import decomposition
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import random

number_of_chapters = 120  # Number of chapters
ignored_words = ["笑道", "宝玉"]  # Words to ignore
randomly_choose_training_samples = False  # Choose training samples for PCA randomly
training_samples_portion = 0.5  # Portion of training samples
adjust_prob = True  # Adjust probability for 1-79 chapters


def main():
    # output_file = open("pca.csv", "w")

    feature_names = []  # Words that are used as features
    counter = word_count_chapters.count_all_chapter()

    # Build data frame
    data_frame = [list() for _ in range(number_of_chapters)]
    for word, counts in counter.items():
        # Filter features
        normalized_variance = word_count_chapters.variance(counts)/(sum(counts)/number_of_chapters)
        if normalized_variance > 0.85 or word in ignored_words:
            continue

        # Add to data frame
        for i in range(number_of_chapters):
            data_frame[i].append(counts[i])
        feature_names.append(word)

        # output_file.write("%s,%f\n" % (word, normalized_variance))
    data_frame = np.array(data_frame)

    # output_file.close()
    # exit()

    # Start PCA
    while True:
        pca = decomposition.PCA(n_components=3, whiten=True, svd_solver="full")
        pca.fit(split_data(data_frame))
        result = pca.transform(data_frame)

        save_components(pca.components_, feature_names)

        print("Explained variance ratio:", pca.explained_variance_ratio_)
        print("Features:", feature_names)
        print("Number of Features:", len(feature_names))

        # save_result_csv(result, output_file)

        plot_result(result)


def split_data(data_frame, prob=0.5):
    if not randomly_choose_training_samples:
        print("Training chapters: all")
        return data_frame

    training_data = []
    training_chapters = []
    for i, line in enumerate(data_frame):
        if adjust_prob:
            adjusted_prob = prob/2 if i < 80 else prob
        else:
            adjusted_prob = prob

        if random.random() < adjusted_prob:
            training_data.append(line)
            training_chapters.append(i)

    print("Training chapters:", training_chapters)
    return np.array(training_data)


def save_components(components, features):
    output_file = open("components.csv", "w")
    for i, feature in enumerate(features):
        output_file.write("%s," % feature)
        for component in components:
            output_file.write("%f," % component[i])
        output_file.write("\n")


def plot_result(result):
    figure = plt.figure()
    # plot = figure.add_subplot(111)
    plot = Axes3D(figure)
    plot.set_xlabel("component 1")
    plot.set_ylabel("component 2")
    plot.set_zlabel("component 3")

    for i, line in enumerate(result):
        # r = min(i/60, 1)
        # g = min(2-i/60, 1)
        # b = 0
        #
        # r, g = g, r
        #
        # color = (r, g, b, 0.5)

        # if i > 80:
        #     marker = "s"
        #     color = "b"
        # elif i > 40:
        #     marker = "^"
        #     color = "r"
        # else:
        #     marker = "o"
        #     color = "g"
        marker = "o"
        alpha = 0.5

        if i > 80:
            color = (0, 0, 1, alpha)
        elif i > 40:
            color = (0, 1, 0, alpha)
        else:
            color = (1, 0, 0, alpha)

        # if i > 100:
        #     color = (1, 0, 1, alpha)
        # elif i > 80:
        #     color = (0, 0, 1, alpha)
        # elif i > 60:
        #     color = (0, 1, 1, alpha)
        # elif i > 40:
        #     color = (0, 1, 0, alpha)
        # elif i > 20:
        #     color = (1, 1, 0, alpha)
        # else:
        #     color = (1, 0, 0, alpha)

        # plot.text(line[0], line[1], str(i+1), size=10, ha="center", va="center")
        # plot.scatter(line[0], line[1], marker=marker, c=color, s=200, linewidths=0)

        plot.text(line[0], line[1], line[2], str(i+1), size=10, ha="center", va="center")
        plot.scatter(line[0], line[1], line[2], marker=marker, c=color, s=200, linewidths=0)
    plt.show()

if __name__ == '__main__':
    main()
