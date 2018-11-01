import _taggerHelpers as helpers
from _taggerGlobal import REPLACE_AUTHOR_STRING
import re


def tag_book(self, is_section):
    self.type[1] = "Bksec" if is_section else "Book"
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

        if seg[-3:] == " pp" and not is_section:
            self.values["pages"][1] = seg[:-3].strip()
            continue
        elif seg[-2:] == " p" and not is_section:
            self.values["pages"][1] = seg[:-2].strip()
            continue

        if segment_tag == None:
            if len(seg) > 9 and seg[:9].upper() == "EDITED BY":
                segment_tag = "editor"
            elif len(seg) > 13 and seg[:13].upper() == "TRANSLATED BY":
                segment_tag = "translator"
            elif len(seg) > 5 and seg[-5] == " vols":
                segment_tag = "number of volumes"
                seg = seg[:-5]
            elif len(seg) > 3 and seg[-3] == " ed":
                segment_tag = "edition"
                seg = seg[:-3]
            else:
                if is_section and last_edit_seg_tag == "book title":
                    segment_tag = "place published"

                if not is_section and last_edit_seg_tag == "title":
                    segment_tag = "place published"

        if segment_tag == "place published":

            # if it is a book section, we need to go back and get pages
            if is_section:
                last_seg = self.values[last_edit_seg_tag][1]
                last_seg_comma_i = last_seg.rfind(",")
                if last_seg_comma_i == -1:
                    self.error = True
                    self.error_message = "Tagged as book section but couldn't find comma for pages"
                else:
                    self.values[last_edit_seg_tag][1] = last_seg[:last_seg_comma_i]
                    page_string = last_seg[last_seg_comma_i + 1:]
                    page_string_colon_i = page_string.find(":")
                    if page_string_colon_i == -1:
                        self.values["pages"][1] = page_string
                    else:
                        self.values["pages"][1] = page_string[page_string_colon_i + 1:]
                        self.values["volume"][1] = page_string[:page_string_colon_i]
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
                segment_tag = None
            elif segment_tag == "translated title":
                segment_tag = None
            else:
                self.error = True
                break
            italics_detected += 1
        elif "</i>" in seg and segment_tag == "book title":
            self.values["book title"][1] = seg.strip()
            last_edit_seg_tag = segment_tag
            segment_tag = "place published"
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
