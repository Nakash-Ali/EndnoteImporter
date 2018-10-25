from _taggerGlobal import TAGGING_SYMBOL
from _taggerGlobal import THESIS_DISS_INDICATORS
import _taggerHelpers as helpers

def tag_ref_type(self):
    title_in_quotes = False
    italics_detected = False

    segments = self.segments
    for i, seg in enumerate(segments):
        seg = seg.strip()
        if len(seg) == 0:
            continue
        if (seg[0] == "\"") or (seg[0] == "\'"):
            title_in_quotes = True
        elif seg[:3] == "<i>":
            if title_in_quotes:
                italics_detected = True
            else:
                self.tag_book(False)
                return

        if title_in_quotes and seg[:2] == "In":
            self.tag_book(True)
            return

    if title_in_quotes:
        if italics_detected:
            self.tag_journal_article()
        else:
            has_thesis_indicators = False
            for inds in THESIS_DISS_INDICATORS:
                if helpers.check_for_string(inds, segments):
                    has_thesis_indicators = True
                    break

            if has_thesis_indicators:
                self.tag_thesis()
            else:
                self.error = True
                self.error_message = "No Thesis Indicators Present"
    else:
        self.error = True
        self.error_message = "Couldn't Match to Existing Ref Types"


def output(self, file):
    if self.type[1] is not None:
        file.write(TAGGING_SYMBOL + self.type[0] + " " + self.type[1] + "\n")
        vals = self.values
        for key in vals.keys():
            if vals[key][1]:
                file.write(TAGGING_SYMBOL + vals[key][0] + " " + vals[key][1] + "\n")
        file.write("\n")


functions = [tag_ref_type, output]