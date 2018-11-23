import os
from constants.Configuration import FILE_LOC_STYLE, SETTINGS_VAR_STYLE, FILE_TYPE_STYLE, FILE_PATH_SETTINGS, \
    FILE_PATH_FIELD_TAGS, FILE_PATH_REF_TAGS


# Returns the file which contains the bib style definition, based on the settings file
def get_style_def_file():
    # Get the bib format from the settings file
    try:
        settings_file = open(FILE_PATH_SETTINGS, "r")
    except:
        raise Exception("Error: Couldn't find a settings.txt file")
    bib_format = None
    style_file = None
    for line in settings_file.readlines():
        values = line.split("=")
        # Get specified style from settings
        if values[0].upper().strip() == SETTINGS_VAR_STYLE.upper():
            bib_format = values[1].strip()

            # Look for the user-specified style in the styles folder
            style_file_names = os.listdir(FILE_LOC_STYLE)
            for fn in style_file_names:
                slice_i = -1 * len(FILE_TYPE_STYLE)
                if fn[slice_i:] == FILE_TYPE_STYLE and fn[:slice_i] == bib_format:
                    input_file_path = FILE_LOC_STYLE + bib_format + FILE_TYPE_STYLE
                    style_file = open(input_file_path, "r")
                    break
            break

    # Check for errors in above parse
    if bib_format is None:
        raise Exception("Error: No style was specified in the settings file")
    elif style_file is None:
        raise Exception("Error: Couldn't find a {} file in the styles folder".format(bib_format + FILE_TYPE_STYLE))
    else:
        return style_file


def get_field_tags_file():
    try:
        field_tags_file = open(FILE_PATH_FIELD_TAGS, "r")
    except:
        raise Exception("Error: Couldn't find a field_tags.txt file in a tags folder")
    return field_tags_file


def get_reference_tags_file():
    try:
        reference_tags_file = open(FILE_PATH_REF_TAGS, "r")
    except:
        raise Exception("Error: Couldn't find a reference_tags.txt file in a tags folder")
    return reference_tags_file


def file_to_dictionary(file, key_val_splitter=":"):
    out_dict = {}
    for line in file.readlines():
        elements = line.split(key_val_splitter, 1)
        if len(elements) < 2:
            raise Exception("Error: Couldn't convert {} to a Python dictionary.".format(file.name))
        else:
            out_dict[elements[0]] = elements[1]
    return out_dict