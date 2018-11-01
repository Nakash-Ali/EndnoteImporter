import _taggerHelpers as helpers
from _taggerGlobal import REPLACE_AUTHOR_STRING


def tag_journal_article(self):
    self.type[1] = "Jouart"
    author = ""
    italics_detected = 0
    quotes_detected = 0
    type_of_quotes = ""

    segments = self.segments
    segment_tag = None
    for i, seg in enumerate(segments):
        seg = seg.strip()
        if len(seg) == 0:
            continue

        if (seg[0] == "\"") or (seg[0] == "\'"):
            type_of_quotes = seg[0]
            if quotes_detected == 0:
                author = helpers.get_author(segments, i)
                segment_tag = "title"
            else:
                self.error = True

        if seg[:3] == "<i>":
            if italics_detected == 0:
                # start adding to title string
                segment_tag = "journal"
            else:
                self.error = True

        if seg[:6] == "Review":
            segment_tag = "reviewed item"

        if segment_tag == "issue":
            open_bracket_i = seg.find("(")
            if open_bracket_i != -1:
                if not seg[0].isdigit() and open_bracket_i != 0:
                    self.error = True
                self.values["issue"][1] = seg[:open_bracket_i].strip()
                seg = seg[open_bracket_i:]
                if seg[-1] == ")" and helpers.check_for_year([seg[1:-1]], True):
                    self.values["year"][1] = seg[1:-1]
                else:
                    self.error = True
                    self.error_message = "Tagged as journal article but couldn't find year"
                    print(self.line)
                    break
                segment_tag = "pages"
                continue
            else:
                self.error = True
                segment_tag = None

        if segment_tag:
            if self.values[segment_tag][1]:
                self.values[segment_tag][1] += seg.strip()
            else:
                self.values[segment_tag][1] = seg.strip()

        if segment_tag == "volume":
            if not seg[0].isdigit():
                self.error = True
            segment_tag = "issue"

        if segment_tag == "pages":
            segment_tag = "notes"

        if "</i>" in seg and segment_tag == "journal":
            self.values["journal"][1], journal_info = helpers.italics_trimmer(self.values["journal"][1], seg)
            info_segments = journal_info.split(":")
            for j, s in enumerate(info_segments):
                segments.insert(i+1+j, s)
            if len(info_segments) == 3:
                segment_tag = "volume"
            elif len(info_segments) == 2:
                segment_tag = "issue"
            else:
                segment_tag = None
                self.error = True

        if seg[-1] == type_of_quotes:
            segment_tag = "translated title"
            quotes_detected += 1

    self.values["title"][1] = ((self.values["title"][1].strip())[1:])[:-1]

    self.values["journal"][1] = ((self.values["journal"][1].strip())[3:])[:-4]

    if author == REPLACE_AUTHOR_STRING:
        self.replace_author = True
    self.values["author"][1] = author


functions = [tag_journal_article]


