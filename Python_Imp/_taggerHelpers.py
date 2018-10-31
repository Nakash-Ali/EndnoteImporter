import errno
import os
import re
import docx

from datetime import date
from _taggerGlobal import OUTPUT_FILE_LOC, OUTPUT_FILE_SUFFIX, ERROR_FILE_LOC, ERROR_FILE_SUFFIX, \
    ITAL_TAGGED_FILE_LOC, MAX_LENGTH_FILENAME, INPUT_FILE_LOC, ITAL_TAGGED_FILE_SUFFIX


def check_for_string(str, segments):
    for seg in segments:
        if str in seg:
            return True
    return False


def check_for_year(segments, is_strict):
    for seg in segments:
        seg = seg.strip()
        try:
            years = []
            current_year = int(date.today().year)
            years.append(int(seg[-4:]))

            if is_strict and len(seg) > 4:
                years.append(int(seg[:4]))

            valid_years = True
            for year in years:
                if year > current_year:
                    valid_years = False
                    break
            if not valid_years:
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


def create_file_if_none(filename):
    if len(filename) > MAX_LENGTH_FILENAME:
        filename = filename[-1 * MAX_LENGTH_FILENAME:]

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return filename


def get_files(file_name):
    if file_name[-4:] == ".txt":
        file_prefix = file_name[:-4]
        out_file_name = create_file_if_none( OUTPUT_FILE_LOC + file_prefix + OUTPUT_FILE_SUFFIX )
        err_file_name = create_file_if_none( ERROR_FILE_LOC + file_prefix + ERROR_FILE_SUFFIX )

        file = open(ITAL_TAGGED_FILE_LOC + file_name, "r", encoding="utf8")
        out_file = open(out_file_name, "w", encoding="utf8")
        err_file = open(err_file_name, "w", encoding="utf8")
        return (file, out_file, err_file)


def preprocess_line(line):
    line = re.sub("</i>\s*<i>", " ", line)
    line = line.replace("“", "\"")
    line = line.replace("”", "\"")
    line = line.replace(".\"", "\".")
    line = line.replace(",\"", "\",")
    line = line.replace(".</i>", "</i>.")
    return line


def tag_talics():
    file_names = os.listdir(INPUT_FILE_LOC)
    for doc_file_name in file_names:
        if doc_file_name[-5:] == ".docx":
            file_prefix = doc_file_name[:-5]
            ital_file_name = create_file_if_none(ITAL_TAGGED_FILE_LOC + file_prefix + ITAL_TAGGED_FILE_SUFFIX )
            ital_out_file = open(ital_file_name, "w", encoding="utf8")

            doc = docx.Document(INPUT_FILE_LOC + doc_file_name)
            for para in doc.paragraphs:
                if para.text.strip() == "":
                    continue
                runs = para.runs
                text = ""
                for i, run in enumerate(runs):
                    if (i == 0 or not runs[i-1].italic) and (run.italic):
                        text += "<i>"

                    text += run.text

                    if (i == len(runs) - 1 or not runs[i+1].italic) and (run.italic):
                        text += "</i>"
                ital_out_file.write(text + "\n")
                    #print(run.text, run.italic)