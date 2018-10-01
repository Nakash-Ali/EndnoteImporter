from datetime import date
from enum import Enum
import re

TAGGING_SYMBOL = "%"
REPLACE_AUTHOR_STRING = "___"


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


class Reference:
    def __init__(self, line):
        self.line = line
        self.segments = line.split(".")
        self.replace_author = False
        self.error = False
        self.type = ["0", None]
        self.values = {
            "author": ["A", None],
            "year": ["D", None],
            "title": ["T", None],
            "pages": ["P", None],
            "place published": ["C", None],
            "publisher": ["I", None],
            "translated title": ["Q", None],
            "editor": ["E", None],
            "translator": ["Y", None],
            "notes": ["Z", None]
        }

        # Combine segments which are separated due to appreviations e.g. N. A. Babwany should be 1 segment
        for i, seg in enumerate(self.segments):
            while (
                    (len(seg) > 1 and not seg[-2].isalnum() )
                    or len(seg) == 1
            ) \
                    and seg[-1].isupper() \
                    and i < len(self.segments) - 1 \
                    and self.segments[i + 1].strip()[0] != "\"" \
                    and self.segments[i + 1].strip()[0] != "\'" \
                    and self.segments[i + 1].strip()[0] != "<":
                self.segments[i] += "." + self.segments[i + 1]
                self.segments.pop(i + 1)
                seg = self.segments[i]

    def tag_book(self):
        self.type[1] = "Book"
        author = ""
        italics_detected = 0

        segments = self.segments
        segment_tag = None
        for i, seg in enumerate(segments):
            if "<i>" in seg:
                if italics_detected == 0:
                    # get author from previous segments
                    j = 0
                    while j < i:
                        author += segments[j]
                        if i - j > 1:
                            author += "."
                        j += 1

                    # start adding to title string
                    segment_tag = "title"
                else:
                    segment_tag = "translated title"

            if seg[-3:] == " pp":
                self.values["pages"][1] = seg[:-3].strip()
                continue
            elif seg[-2:] == " p":
                self.values["pages"][1] = seg[:-2].strip()
                continue

            if segment_tag == "editor" and not bool(re.search("Edited .* by", seg)):
                segment_tag = "translator"

            if segment_tag == "translator" and not bool(re.search("Translated .* by", seg)):
                segment_tag = "place published"

            if segment_tag == "place published":
                colon_pos = seg.find(":")
                if colon_pos != -1:
                    self.values[segment_tag][1] = seg[:colon_pos].strip()
                    seg = seg[colon_pos + 1:]
                segment_tag = "publisher"

            if segment_tag == "publisher":
                comma_pos = seg.find(",")
                if comma_pos != -1:
                    self.values[segment_tag][1] = seg[:comma_pos].strip()
                    seg = seg[comma_pos + 1:]
                segment_tag = "year"

            if segment_tag == "year":
                if check_for_year([seg]):
                    self.values[segment_tag][1] = seg.strip()
                else:
                    self.error = True
                    break
                segment_tag = "notes"


            if segment_tag:
                if self.values[segment_tag][1]:
                    self.values[segment_tag][1] += seg.strip()
                else:
                    self.values[segment_tag][1] = seg.strip()

            if "</i>" in seg:
                if segment_tag == "title":
                    segment_tag = "editor"
                elif segment_tag == "translated title":
                    segment_tag = "place published"
                else:
                    self.error = True
                    break

        # trim everything
        author = author.strip()
        if author == REPLACE_AUTHOR_STRING:
            self.replace_author = True
        self.values["title"][1] = ((self.values["title"][1].strip())[3:])[:-4]  # remove the italic tags
        self.values["author"][1] = author

    def tag_ref_type(self):
        # possible_types = {}
        # for r in REF_TYPES:
        #     possible_types[r] = True

        segments = self.segments
        for i, seg in enumerate(segments):
            seg = seg.strip()
            if len(seg) == 0:
                continue
            if (seg[0] == "\"") or (seg[0] == "\'"):
                self.error = True
            elif "<i>" in seg:
                if check_for_year(segments[i + 1:]):
                    self.tag_book()
                    break
                else:
                    self.error = True

        if self.type is None:
            self.error = True

    def output(self, file):
        if self.type[1] is not None:
            file.write(TAGGING_SYMBOL + self.type[0] + " " + self.type[1] + "\n")
            vals = self.values
            for key in vals.keys():
                if vals[key][1]:
                    file.write(TAGGING_SYMBOL + vals[key][0] + " " + vals[key][1] + "\n")
            file.write("\n")


# REF_TYPES = [
#     "Book",
#     "Book Section",
#     "Journal Article",
#     "Thesis",
#     "Manuscript"
# ]


def preprocess_line(line):
    line = re.sub("</i>\s*<i>", " ", line)
    line = line.replace("“", "\"")
    line = line.replace("”", "\"")
    line = line.replace(".\"", "\".")
    line = line.replace(".</i>", "</i>.")
    return line


def no_tag():
    return "no tag todo"


def main():
    file = open("jiwa-untagged.txt", "r", encoding="utf8")
    out_file = open("output.txt", "w", encoding="utf8")
    err_file = open("errors.txt", "w", encoding="utf8")
    references = []

    for i, line in enumerate(file.readlines()):
        ref = Reference(preprocess_line(line))
        ref.tag_ref_type()
        references.append(ref)

    count = 0
    for i, reference in enumerate(references):
        if not reference.error:
            if reference.replace_author and i > 0:
                reference.values["author"][1] = references[i - 1].values["author"][1]
            reference.output(out_file)
            count += 1
        else:
            err_file.write(reference.line)

    print(count)

    #return tag_ref_type(file.readline())


main()
