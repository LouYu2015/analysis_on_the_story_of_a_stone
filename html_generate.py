import locale
import urllib.request
import os

input_file = open("word_count.csv", "r")
result_folder = "html"

if not os.path.exists(result_folder):
    os.mkdir(result_folder)

output_index = open(os.path.join(result_folder, "index.html"), "w")
output_expanded = open(os.path.join(result_folder, "expanded.html"), "w")

locale.setlocale(locale.LC_COLLATE, "zh_CN.UTF8")


def load_data():
    lines = input_file.read().split("\n")
    result = []
    for line in lines:
        if not line:
            continue

        cols = line.split(",")
        if not cols[0]:
            continue

        result.append([cols[0], int(cols[1])])
    return result


def sorted_table(table):
    return sorted(table, key=lambda x: locale.strxfrm(x[0]))


def generate_index(table):
    last_char = ''
    result = []
    for line in table:
        current_char = line[0][0]
        current_label = urllib.request.pathname2url(current_char)
        if current_char != last_char:
            result.append('<h1 id="%s">%s<a href="%s#%s">[展开]</a></h1>' %
                          (current_label, current_char, "expanded.html", current_label))
        last_char = current_char
    return ''.join(result)


def generate_expanded(table):
    last_char = ''
    result = []
    for line in table:
        current_char = line[0][0]
        current_label = urllib.request.pathname2url(current_char)
        if current_char != last_char:
            result.append('<h1 id="%s">%s<a href="%s#%s">[收起]</a></h1>' %
                          (current_label, current_char, "index.html", current_label))

        result.append('<h2>%s(%d)</h2>' % (line[0], line[1]))

        last_char = current_char
    return ''.join(result)


def apply_template(string):
    template = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="styles.css">
<title>红楼词表 第二版</title>
</head>
<body>
<header><p>红楼词表</p></header>
%s
<div id="copyright">
<p><a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />
本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。<br>
Copyright 2017 Yu Lou(楼宇). Some rights reserved.<br>
2017 年 8 月 20 日更新
</p><br>
访客计数： 

<!-- Start of StatCounter Code for Default Guide -->
<script type="text/javascript">
var sc_project=11426958; 
var sc_invisible=0; 
var sc_security="a175aef9"; 
var scJsHost = (("https:" == document.location.protocol) ?
"https://secure." : "http://www.");
document.write("<sc"+"ript type='text/javascript' src='" +
scJsHost+
"statcounter.com/counter/counter.js'></"+"script>");
</script>
<noscript><div class="statcounter"><a title="web analytics"
href="http://statcounter.com/" target="_blank"><img
class="statcounter"
src="//c.statcounter.com/11426958/0/a175aef9/0/" alt="web
analytics"></a></div></noscript>

</p>
</div>
</body>
</html>
'''
    return template % string


def main():
    lines = sorted_table(load_data())
    output_index.write(apply_template(generate_index(lines)))
    output_expanded.write(apply_template(generate_expanded(lines)))

if __name__ == '__main__':
    main()
