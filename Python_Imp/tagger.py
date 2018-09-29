from datetime import date
import re

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
    return line


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


def no_tag():
    return "no tag todo"


def tag_book(segments):
    author = ""
    title = ""
    italics_detected = 0

    add_to_title = False
    for i, seg in enumerate(segments):
        if "<i>" in seg:
            if italics_detected == 0:
                # get author from previous segments
                j = 0
                while j < i:
                    author += segments[j]
                    if i - j > 1:
                        author += "."
                    j+=1

                # start adding to title string
                add_to_title = True

        if add_to_title:
            title += seg

        if "</i>" in seg:
            add_to_title = False
            italics_detected+=1

    # trim everything
    author = author.strip()
    title = ((title.strip())[3:])[:-4]  # remove the italic tags
    return {author, title}


def tag_ref_type(line):
    # possible_types = {}
    # for r in REF_TYPES:
    #     possible_types[r] = True

    segments = line.split(".")
    found = False
    for i, seg in enumerate(segments):
        if ("\"" in seg) or ("\'" in seg):
            return False
        elif "<i>" in seg:
            if check_for_year(segments[i+1:]):
                return tag_book(segments)
            else:
                return False
    return False


def main():
    file = open("jiwa-untagged.txt", "r", encoding="utf8")
    out_file = open("output.txt", "w", encoding="utf8")

    for line in file.readlines():
        line = preprocess_line(line)
        result = tag_ref_type(line)
        if result:
            print(result)

    #return tag_ref_type(file.readline())


main()
