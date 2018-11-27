from constants.Configuration import FILE_LOC_INPUT, FILE_LOC_ITAL, FILE_SUFFIX_ITAL
from helpers.Output import create_file_if_none
import re
import os
import docx


def preprocess_line(line):
    line = re.sub("</i>\s*<i>", " ", line)
    line = line.replace("“", "\"")
    line = line.replace("”", "\"")
    return line


def tag_talics():
    file_names = os.listdir(FILE_LOC_INPUT)
    for doc_file_name in file_names:
        if doc_file_name[-5:] == ".docx":
            file_prefix = doc_file_name[:-5]
            ital_file_name = create_file_if_none(FILE_LOC_ITAL + file_prefix + FILE_SUFFIX_ITAL )
            ital_out_file = open(ital_file_name, "w", encoding="utf8")

            doc = docx.Document(FILE_LOC_INPUT + doc_file_name)
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