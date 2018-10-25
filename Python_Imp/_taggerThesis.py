import _taggerHelpers as helpers
from _taggerGlobal import REPLACE_AUTHOR_STRING


def tag_thesis(self):
    self.type[1] = "Thesis"
    author = ""
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
                self.error_message = "Tagged as thesis but more than one pair of quotes"
                print(self.line)
                break

        if seg[-3:] == " pp":
            self.values["pages"][1] = seg[:-3].strip()
            continue
        elif seg[-2:] == " p":
            self.values["pages"][1] = seg[:-2].strip()
            continue

        if segment_tag == "thesis type":
            comma_index = seg.find(",")
            if comma_index != -1:
                segments.insert(i + 1, seg[comma_index + 1:])
                seg = seg[:comma_index]
                if self.values[segment_tag][1]:
                    self.values[segment_tag][1] += seg.strip()
                else:
                    self.values[segment_tag][1] = seg.strip()
                segment_tag = "publisher"
                continue
            elif comma_index == -1 and i == len(segments) - 1:
                self.error = True
                self.error_message = "Tagged as thesis but no commas in thesis type"
                break
            else:
                segments[i + 1] = seg + "." + segments[i + 1]
                continue

        if segment_tag == "publisher":
            comma_index = seg.rfind(",")
            if comma_index != -1:
                segments.insert(i + 1, seg[comma_index + 1:])
                seg = seg[:comma_index]
                if self.values[segment_tag][1]:
                    self.values[segment_tag][1] += seg.strip()
                else:
                    self.values[segment_tag][1] = seg.strip()

                segment_tag = "year"
                continue
            elif comma_index == -1 and i == len(segments) - 1:
                self.error = True
                self.error_message = "Tagged as thesis but no commas in "
                break
            else:
                segments[i + 1] = seg + "." + segments[i + 1]
                continue

        if segment_tag == "year":
            if helpers.check_for_year([seg], True):
                self.values[segment_tag][1] = seg.strip()
                segment_tag = "notes"
                continue
            else:
                self.error = True
                self.error_message = "Tagged as thesis but no valid year"
                break

        if segment_tag:
            if self.values[segment_tag][1]:
                self.values[segment_tag][1] += seg.strip()
            else:
                self.values[segment_tag][1] = seg.strip()

        if seg[-1] == type_of_quotes:
            segment_tag = "thesis type"
            quotes_detected += 1

    self.values["title"][1] = ((self.values["title"][1].strip())[1:])[:-1]

    if author == REPLACE_AUTHOR_STRING:
        self.replace_author = True
    self.values["author"][1] = author

    if self.values["title"][1] is None:
        self.error = True
        self.error_message = "Tagged as thesis but no segment tag"


functions = [tag_thesis]