import os
from helpers.Output import create_file_if_none
from constants.Configuration import FILE_LOC_STYLE, SETTINGS_VAR_STYLE, FILE_TYPE_STYLE, FILE_PATH_SETTINGS, \
    FILE_PATH_FIELD_TAGS, FILE_PATH_REF_TAGS, FILE_LOC_OUTPUT, FILE_LOC_ERROR, FILE_SUFFIX_OUTPUT, FILE_SUFFIX_ERROR, \
    FILE_LOC_ITAL


def get_settings_file():
    try:
        settings_file = open(FILE_PATH_SETTINGS, "r")
    except:
        raise Exception("Error: Couldn't find a settings.txt file")
    return settings_file


# Returns the file which contains the bib style definition, based on the settings file
def get_style_def_file():
    # Get the bib format from the settings file
    settings_file = get_settings_file()
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


def get_field_tags_dict():
    raw_field_dict = file_to_dictionary(get_field_tags_file())
    new_dict = {}
    for field in raw_field_dict.keys():
        new_key = field.strip().replace(" ", "_")
        new_dict[new_key] = raw_field_dict[field]
    return new_dict


def get_reference_tags_file():
    try:
        reference_tags_file = open(FILE_PATH_REF_TAGS, "r")
    except:
        raise Exception("Error: Couldn't find a reference_tags.txt file in a tags folder")
    return reference_tags_file


def file_to_dictionary(file, key_val_splitter=":"):
    out_dict = {}
    for line in file.readlines():
        line = line.strip()
        # ignore commented lines
        if len(line) > 0 and line[0] != "#":
            elements = line.split(key_val_splitter, 1)
            if len(elements) < 2:
                raise Exception("Error: Couldn't convert {} to a Python dictionary.".format(file.name))
            else:
                out_dict[elements[0].strip()] = elements[1].strip()
    return out_dict


def get_bib_files(file_name):
    if file_name[-4:] == ".txt":
        file_prefix = file_name[:-16] if len(file_name) > 16 else file_name
        out_file_name = create_file_if_none( FILE_LOC_OUTPUT + file_prefix + FILE_SUFFIX_OUTPUT )
        err_file_name = create_file_if_none( FILE_LOC_ERROR + file_prefix + FILE_SUFFIX_ERROR )

        file = open(FILE_LOC_ITAL + file_name, "r", encoding="utf8")
        out_file = open(out_file_name, "w", encoding="utf8")
        err_file = open(err_file_name, "w", encoding="utf8")
        return (file, out_file, err_file)
