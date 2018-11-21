from helpers import GetInputFiles as file_getter
from helpers.ParseBibFormat import replace_field_tags, replace_ci_tags, replace_opt_tags, replace_quote_tags
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
    reg_ex = convert_line_to_regex(file.readline())  # convert into a reg_ex string
    return {}


def output():
    return "TODO"


def main():
    input_file = file_getter.get_style_def_file()   # Get a reference to the styles file
    parse_dict = parse_bib_format(input_file)       # get the parse dictionary of this user defined format

    #res = re.match(reg_ex, ref)