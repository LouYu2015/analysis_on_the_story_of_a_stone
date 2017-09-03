import word_count_chapters
from sklearn import decomposition
import numpy as np
import random

number_of_chapters = 120


def main():
    output_file = open("pca.csv", "w")

    feature = []
    counter = word_count_chapters.count_all_chapter()
    data_frame = [list() for _ in range(number_of_chapters)]
    for word, counts in counter.items():
        normalized_variance = word_count_chapters.variance(counts)/sum(counts)

        if normalized_variance > 0.007 or word in ("笑道", "宝玉"):
            continue

        for i in range(number_of_chapters):
            data_frame[i].append(counts[i])
        feature.append(word)

    data_frame = np.array(data_frame)

    while True:
        pca = decomposition.PCA(n_components=3, whiten=True, svd_solver="full")
        pca.fit(split_data(data_frame))
        result = pca.transform(data_frame)

        print(pca.explained_variance_ratio_)
        save_components(pca.components_, feature)

        print(feature)
        print(len(data_frame[0]))

        # save_result_csv(result, output_file)

        plot_result(result)


def split_data(data_frame, prob=0.5):
    return data_frame

    training_data = []
    training_lines = []
    for i, line in enumerate(data_frame):
        adjusted_prob = prob/4 if i < 80 else prob

        if random.random() < adjusted_prob:
            training_data.append(line)
            training_lines.append(i)

    print("training lines:", training_lines)
    return np.array(training_data)


def save_result_csv(result, output_file):
    for i, line in enumerate(result):
        if i < 40:
            output_file.write("%f,%f,,\n" % (line[0], line[1]))
        elif i < 80:
            output_file.write("%f,,%f,\n" % (line[0], line[1]))
        else:
            output_file.write("%f,,,%f\n" % (line[0], line[1]))


def save_components(components, features):
    output_file = open("components.csv", "w")
    for i, feature in enumerate(features):
        output_file.write("%s," % feature)
        for component in components:
            output_file.write("%f," % component[i])
        output_file.write("\n")


def plot_result(result):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    figure = plt.figure()
    # plot = figure.add_subplot(111)
    plot = Axes3D(figure)
    plot.set_xlabel("component 1")
    plot.set_ylabel("component 2")
    plot.set_zlabel("component 3")

    for i, line in enumerate(result):
        r = min(i/60, 1)
        g = min(2-i/60, 1)
        b = 0

        r, g = g, r

        color = (r, g, b, 0.5)

        marker = "o"
        # if i > 80:
        #     marker = "s"
        #     color = "b"
        # elif i > 40:
        #     marker = "^"
        #     color = "r"
        # else:
        #     marker = "o"
        #     color = "g"
        alpha = 0.75

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

        plot.text(line[0], line[1], line[2], str(i+1), size=10, ha="center", va="center")
        plot.scatter(line[0], line[1], line[2], marker=marker, c=color, s=200, linewidths=0)
    plt.show()

if __name__ == '__main__':
    main()
