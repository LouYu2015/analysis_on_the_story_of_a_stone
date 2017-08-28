import word_count_chapters
from sklearn import decomposition
import numpy as np

number_of_chapters = 120


def main():
    output_file = open("pca.csv", "w")

    feature = []
    counter = word_count_chapters.count_all_chapter()
    data_frame = [list() for _ in range(number_of_chapters)]
    for word, counts in counter.items():
        normalized_variance = word_count_chapters.variance(counts)/sum(counts)

        if normalized_variance > 0.007:
            continue

        for i in range(number_of_chapters):
            data_frame[i].append(counts[i])
        feature.append(word)

    pca = decomposition.PCA(n_components=2, whiten=True, svd_solver="full")
    result = pca.fit_transform(np.array(data_frame))

    print(feature)
    print(len(data_frame[0]))

    # save_result_csv(result, output_file)

    plot_result(result)


def save_result_csv(result, output_file):
    for i, line in enumerate(result):
        if i < 40:
            output_file.write("%f,%f,,\n" % (line[0], line[1]))
        elif i < 80:
            output_file.write("%f,,%f,\n" % (line[0], line[1]))
        else:
            output_file.write("%f,,,%f\n" % (line[0], line[1]))


def plot_result(result):
    import matplotlib
    import matplotlib.pyplot as plt

    figure = plt.figure()
    plot = figure.add_subplot(111)

    for i, line in enumerate(result):
        r = min(i/60, 1)
        g = min(2-i/60, 1)
        b = 0
        
        r, g = g, r

        color = (r, g, b, 0.5)
        plot.scatter(line[0], line[1], marker=".", c=color, s=500, linewidths=0)

    plt.show()

if __name__ == '__main__':
    main()
