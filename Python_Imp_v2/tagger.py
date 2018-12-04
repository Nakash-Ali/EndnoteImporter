from helpers import GetInputFiles as file_getter
from helpers.ParseBibFormat import replace_field_tags, replace_ci_tags, replace_opt_tags, replace_quote_tags, \
    escape_regex
from helpers import PreprocessInputBib as prep_helpers
from helpers.Output import output_line_for_ref
from constants.StyleDefinitions import REF_TYPE_TAG
from constants.Configuration import FILE_LOC_ITAL
import re
import os


class Reference:
    def __init__(self, line):
        self.line = line
        self.error = False
        self.error_message = None
        self.groupdict = None
        self.reftype_tag = None

    def tag_ref_type(self, PARSE_DICT):
        match_objects = []
        for ref_type in PARSE_DICT.keys():
            for pattern in PARSE_DICT[ref_type]:
                match_obj = re.match(pattern, self.line)
                if match_obj is not None:
                    match_objects.append((ref_type, match_obj))
                    break

        n = len(match_objects)
        if n == 0:
            self.error = True
            self.error_message = "The reference doesn't match any of the reference type formats"
        elif n > 1:
            self.error = True
            self.error_message = "CONFLICT: The reference matches more than one of the reference type formats"
            return 1
        else:
            self.reftype_tag = match_objects[0][0]
            self.groupdict = match_objects[0][1].groupdict()

        return 0


# Given a user defined format for any reference type as a string input, this function converts (and returns)
# the user defined format into a regex based on the Python "re" regular expression library
def convert_line_to_regex(line):
    new_exp = escape_regex(line)
    new_exp = replace_field_tags(new_exp)
    new_exp = replace_ci_tags(new_exp)
    new_exp = replace_opt_tags(new_exp)
    new_exp = replace_quote_tags(new_exp)
    return new_exp


# This method returns a dictionary (i.e. the parse dictionary) where the keys are the reference type tags
# e.g. "Jouart" for Journal Articles and the values are arrays of regex strings which are considered valid matches of
# that reference type (those regexes are built based on the bib style file passed in as an input file to this function)
def parse_bib_format(file, REF_TAG_DICT):
    current_ref_type = None
    parse_dict = {}
    for line in file.readlines():
        # If it is a line starting with "---ref_type:", extract the ref_type from that line and add it as a new key
        # in the parse dictionary
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            continue
        elif line[:len(REF_TYPE_TAG)] == REF_TYPE_TAG:
            ref_type_str = line[len(REF_TYPE_TAG):]
            ref_type_str = ref_type_str.strip()
            if REF_TAG_DICT[ref_type_str] is not None:
                current_ref_type = REF_TAG_DICT[ref_type_str].strip()
                # empty list of regexes which we will add to as we read following lines
                parse_dict[current_ref_type] = []
            else:
                raise Exception("Error: Couldn't find a corresponding entry for the {} to a Python dictionary.".format(file.name))
        else:
            reg_ex = convert_line_to_regex(line)  # convert into a reg_ex string
            # add this reg_ex to the list of possible match regExps for this reference type in the parse dict
            x = []
            if current_ref_type is not None:
                parse_dict[current_ref_type].append(str(reg_ex))
                x.append(str(reg_ex))
    return parse_dict


def tag_all_input_bibs(PARSE_DICT, FIELD_TAG_DICT):
    x = 0
    prep_helpers.tag_talics()
    file_names = os.listdir(FILE_LOC_ITAL)
    for file_name in file_names:
            file, out_file, err_file = file_getter.get_bib_files(file_name)
            references = []

            for i, line in enumerate(file.readlines()):
                ref = Reference(prep_helpers.preprocess_line(line))
                x += ref.tag_ref_type(PARSE_DICT)
                references.append(ref)

            successes = 0
            count = 0
            for i, reference in enumerate(references):
                if not reference.error:
                    out_file.write(output_line_for_ref(reference.groupdict, FIELD_TAG_DICT, reference.reftype_tag))
                    successes += 1
                else:
                    err_file.write(reference.line)
                    # if reference.error_message is not None:
                    #     print(reference.error_message)
                count += 1

            print(successes, count, x)


def main():
    input_file = file_getter.get_style_def_file()   # Get a reference to the styles file
    REF_TAG_DICT = file_getter.file_to_dictionary(file_getter.get_reference_tags_file())
    FIELD_TAG_DICT = file_getter.get_field_tags_dict()
    PARSE_DICT = parse_bib_format(input_file, REF_TAG_DICT)       # get the parse dictionary of this user defined format
    tag_all_input_bibs(PARSE_DICT, FIELD_TAG_DICT)
    print(PARSE_DICT)


main()