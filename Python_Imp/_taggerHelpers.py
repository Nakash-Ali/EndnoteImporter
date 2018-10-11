import errno
import os
import re
from datetime import date

def check_for_year(segments):
    for seg in segments:
        seg = seg.strip()
        try:
            current_year = int(date.today().year)
            year = int(seg[-4:])
            if year > current_year:
                continue
        except:
            continue
        return True
    return False


def get_author(segments, title_i):
    author = ""
    # get author from previous segments
    j = 0
    while j < title_i:
        author += segments[j]
        if title_i - j > 1:
            author += "."
        j += 1
    author = author.strip()
    return author


def get_files(file_name):
    if file_name[-4:] == ".txt":
        file_prefix = file_name[:-4]
        out_file_name = "./output/" + file_prefix + "_output.txt"
        err_file_name = "./errors/" + file_prefix + "_errors.txt"
        for path in [out_file_name, err_file_name]:
            if not os.path.exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

        file = open("./input/" + file_name, "r", encoding="utf8")
        out_file = open(out_file_name, "w", encoding="utf8")
        err_file = open(err_file_name, "w", encoding="utf8")
        return (file, out_file, err_file)


def preprocess_line(line):
    line = re.sub("</i>\s*<i>", " ", line)
    line = line.replace("“", "\"")
    line = line.replace("”", "\"")
    line = line.replace(".\"", "\".")
    line = line.replace(".</i>", "</i>.")
    return line