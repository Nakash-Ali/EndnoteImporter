import _taggerHelpers as helpers
from _taggerGlobal import REPLACE_AUTHOR_STRING
import re


def tag_book(self, is_section):
    self.type[1] = "Book Section" if is_section else "Book"
    author = ""
    italics_detected = 0
    quotes_detected = 0
    type_of_quotes = ""

    segments = self.segments
    segment_tag = None
    last_edit_seg_tag = None
    for i, seg in enumerate(segments):
        seg = seg.strip()
        if len(seg) == 0:
            continue

        if (seg[0] == "\"") or (seg[0] == "\'") and is_section:
            type_of_quotes = seg[0]
            if quotes_detected == 0:
                author = helpers.get_author(segments, i)
                segment_tag = "title"
            elif quotes_detected == 1:
                segment_tag = "chapter"
            else:
                segment_tag = "translated title"

        if seg[:2] == "In" and is_section:
            seg = seg[2:].strip()
            segment_tag = "book title"

        if seg[:3] == "<i>" and not is_section:
            if italics_detected == 0:
                author = helpers.get_author(segments, i)
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
            segment_tag = "edition"

        if segment_tag == "edition" and not seg[-2:] == "ed":
            segment_tag = "number of volumes"

        if segment_tag == "number of volumes" and not

        if segment_tag == "place published":
            colon_pos = seg.find(":")
            if colon_pos != -1:
                self.values[segment_tag][1] = seg[:colon_pos].strip()
                last_edit_seg_tag = segment_tag
                seg = seg[colon_pos + 1:]
            segment_tag = "publisher"

        if segment_tag == "publisher":
            comma_pos = seg.find(",")
            if comma_pos != -1:
                self.values[segment_tag][1] = seg[:comma_pos].strip()
                last_edit_seg_tag = segment_tag
                seg = seg[comma_pos + 1:]
            segment_tag = "year"

        if segment_tag == "year":
            if helpers.check_for_year([seg], False):
                self.values[segment_tag][1] = seg.strip()
                last_edit_seg_tag = segment_tag
            else:
                self.error = True
                self.error_message = "Tagged as book section but couldn't find year" if is_section \
                    else "Tagged as book but couldn't find year"
                break
            segment_tag = "notes"
            continue

        if segment_tag:
            if self.values[segment_tag][1]:
                self.values[segment_tag][1] += seg.strip()
            else:
                self.values[segment_tag][1] = seg.strip()
            last_edit_seg_tag = segment_tag

        if seg[-1] == type_of_quotes and is_section:
            if segment_tag == "title" or segment_tag == "chapter":
                segment_tag = None
            elif segment_tag == "translated title":
                segment_tag = "place published"
            else:
                self.error = True
                break
            quotes_detected += 1

        if seg[-4:] == "</i>":
            if segment_tag == "title" or segment_tag == "book title":
                segment_tag = "editor"
            elif segment_tag == "translated title":
                segment_tag = "edition"
            else:
                self.error = True
                break
            italics_detected += 1
        elif "</i>" in seg and segment_tag == "book title":
            self.values["book title"][1] = seg.strip()
            last_edit_seg_tag = segment_tag
            segment_tag = "editor"
            italics_detected += 1

    # trim everything
    self.values["title"][1] = ((self.values["title"][1].strip())[1:])[:-1] if is_section else \
        ((self.values["title"][1].strip())[3:])[:-4]  # remove the italic tags

    if author == REPLACE_AUTHOR_STRING:
        self.replace_author = True
    self.values["author"][1] = author

    if is_section and self.values["book title"][1]:
        self.values["book title"][1] = ((self.values["book title"][1].strip())[3:])[:-4]


functions = [tag_book]
