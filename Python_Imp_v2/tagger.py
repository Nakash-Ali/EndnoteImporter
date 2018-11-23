from helpers import GetInputFiles as file_getter
from helpers.ParseBibFormat import replace_field_tags, replace_ci_tags, replace_opt_tags, replace_quote_tags
from constants.StyleDefinitions import REF_TYPE_TAG
import re


# Given a user defined format for any reference type as a string input, this function converts (and returns)
# the user defined format into a regex based on the Python "re" regular expression library
def convert_line_to_regex(line):
    new_exp = re.escape(line)
    new_exp = replace_field_tags(new_exp)
    new_exp = replace_ci_tags(new_exp)
    new_exp = replace_opt_tags(new_exp)
    new_exp = replace_quote_tags(new_exp)
    return new_exp


# This method returns a dictionary (i.e. the parse dictionary) where the keys are the reference type tags
# e.g. "Jouart" for Journal Articles and the values are arrays of regex strings which are considered valid matches of
# that reference type (those regexes are built based on the bib style file passed in as an input file to this function)
def parse_bib_format(file):
    REF_TAG_DICT = file_getter.file_to_dictionary(file_getter.get_reference_tags_file())
    current_ref_type = None
    parse_dict = {}
    for line in file.readlines():
        # If it is a line starting with "---ref_type:", extract the ref_type from that line and add it as a new key
        # in the parse dictionary
        line = line.strip()
        if line[:len(REF_TYPE_TAG)] == REF_TYPE_TAG:
            ref_type_str = line[len(REF_TYPE_TAG):]
            ref_type_str = ref_type_str.strip()
            if REF_TAG_DICT[ref_type_str] is not None:
                current_ref_type = REF_TAG_DICT[ref_type_str]
                # empty list of regexes which we will add to as we read following lines
                parse_dict[current_ref_type] = []
            else:
                raise Exception("Error: Couldn't find a corresponding entry for the {} to a Python dictionary.".format(file.name))
        else:
            reg_ex = convert_line_to_regex(file.readline())  # convert into a reg_ex string
            # add this reg_ex to the list of possible match regExps for this reference type in the parse dict
            if current_ref_type is not None:
                parse_dict[current_ref_type].append(reg_ex)
    return parse_dict


def output():
    return "TODO"


def main():
    input_file = file_getter.get_style_def_file()   # Get a reference to the styles file
    parse_dict = parse_bib_format(input_file)       # get the parse dictionary of this user defined format

    #res = re.match(reg_ex, ref)

f = open("styles/testFormat.txt", "r")
print(parse_bib_format(f))