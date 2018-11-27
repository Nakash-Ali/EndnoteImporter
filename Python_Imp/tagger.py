import _taggerBook
import _taggerLib
import _taggerReference
import _taggerJournalArticle
import _taggerThesis
import os

from _taggerHelpers import get_files, preprocess_line, tag_talics
from _taggerGlobal import ITAL_TAGGED_FILE_LOC


@_taggerLib.add_functions_as_methods(_taggerBook.functions)
@_taggerLib.add_functions_as_methods(_taggerReference.functions)
@_taggerLib.add_functions_as_methods(_taggerJournalArticle.functions)
@_taggerLib.add_functions_as_methods(_taggerThesis.functions)

class Reference:
    def __init__(self, line):
        self.line = line
        self.segments = line.split(".")
        self.replace_author = False
        self.error = False
        self.error_message = None
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
            "notes": ["Z", None],
            "book title": ["B", None],
            "journal": ["J", None],
            "volume": ["V", None],
            "issue": ["N", None],
            "reviewed item": ["*", None],
            "chapter": ["&", None],
            "thesis type": ["9", None],
            "number of volumes": ["6", None],
            "edition": ["7", None]
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


def main():
    tag_talics()
    file_names = os.listdir(ITAL_TAGGED_FILE_LOC)
    for file_name in file_names:
            file, out_file, err_file = get_files(file_name)
            references = []

            for i, line in enumerate(file.readlines()):
                ref = Reference(preprocess_line(line))
                ref.tag_ref_type()
                references.append(ref)

            successes = 0
            count = 0
            for i, reference in enumerate(references):
                if not reference.error:
                    if reference.replace_author and i > 0:
                        reference.values["author"][1] = references[i - 1].values["author"][1]
                    reference.output(out_file)
                    successes += 1
                else:
                    err_file.write(reference.line)
                    if reference.error_message is not None:
                        print(reference.error_message)
                count += 1

            print(successes, count)


main()