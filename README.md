# Analysis on *the Story of a Stone*

Author: Yu Lou

Written for Python 3.

## preprocess.py

Preprocess text.

### Input

* hlm.txt: original text

### Output

* preprocessing.txt: preprocessed text.

## preprocess_chapters.py

Split text into chapters and preprocess them.

### Input

* hlm.txt: original text

### Output

* chapters(folder): preprocessed text. One file for each chapter, numbered from "1.text".

## dict_creat.py

Creat dictionary.

### Input

* preprocessing.txt: preprocessed text.

### Output

* dict.csv: dictionary.

## word_split.py

Split words apart.

### Input

* preprocessing.txt: preprocessed text.
* dict.csv: dictionary.

### Output

* word_split.text: splitted text.

## word_split_chapters.py

Split words apart in all chapters.

### Input

* preprocessing.txt: preprocessed text.
* dict.csv: dictionary.
* chapter(folder): preprocessed text for all chapters.

### Output

* chapter_split(folder): splitted text.  One file for each chapter, numbered from "1.text".

## word_count.py

Count words.

### Input

* word_split.text: splitted text.

### Output

* word_count.csv: counting result, sorted by number of occurence.

## word_count_chapters.py

Count words in each chapters.

### Input

* chapter_split(folder): splitted text for each chapter.

### Output

* word_count_chapters.csv: counting result. One line per word and one chapter per column.

## analysis.py

Do PCA analysis. Show result on screen.

### Prerequisite

"sklearn", "numpy" and "matplotlib" is needed to run this program.

### Input

* word_count_chapters.csv: word counting result for each chapters.

### Output

* components.csv: weights for each components.

## suffix_tree.py

Libary for suffix tree.

## correctness_calculate.py

Calculate the correctness of word splitting algorithm.

### Input

* *_answer.txt: answer.
* *_result.txt: result of the program.

("*" is file prefix)