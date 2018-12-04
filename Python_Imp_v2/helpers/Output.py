from constants.Configuration import OUTPUT_TAGGING_SYMBOL, MAX_LENGTH_FILENAME
from constants.StyleDefinitions import REF_TYPE_OUT_SYMBOL
import os
import errno


# This function takes the match object of the regex and returns the corresponding text output line for that reference
def output_line_for_ref(groupdict, tag_dict, reftype_tag):
    output_str = "{ts}{rt_symbol} {rt_tag}\n".format(ts=OUTPUT_TAGGING_SYMBOL,
                                                   rt_symbol=REF_TYPE_OUT_SYMBOL,
                                                   rt_tag=reftype_tag)
    for key in groupdict.keys():
        if groupdict[key] is not None and groupdict[key].strip() != "":
            field_tag = "{ts}{tag}".format(ts=OUTPUT_TAGGING_SYMBOL, tag=tag_dict[key].strip())
            field_val = groupdict[key]
            field_str = "{ft} {fv}\n".format(ft=field_tag, fv=field_val)
            output_str += field_str
    output_str += "\n"
    return output_str


# Creates a file if there is none with that name. Useful for output and error files
def create_file_if_none(filename):
    if len(filename) > MAX_LENGTH_FILENAME:
        filename = filename[-1 * MAX_LENGTH_FILENAME:]

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return filename