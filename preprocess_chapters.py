import preprocess
import os

chapter_folder = "chapters"  # Folder to save result
chapter_split_mark = "$"  # Split mark to mark the end of chapter

# Create result folder
if not os.path.exists(chapter_folder):
    os.makedirs(chapter_folder)

# Split chapters
string = preprocess.input_file.read()
string = preprocess.str_replace_re(string, "正文 第.{1,5}回", chapter_split_mark)
chapters = string.split(chapter_split_mark)

# Save chapters
for chapter_no, chapter_string in enumerate(chapters):
    if chapter_no == 0:
        continue

    result = preprocess.preprocessing(chapter_string)

    file_name = os.path.join(chapter_folder, "%d.txt" % chapter_no)
    chapter_file = open(file_name, "w")
    chapter_file.write(result)
