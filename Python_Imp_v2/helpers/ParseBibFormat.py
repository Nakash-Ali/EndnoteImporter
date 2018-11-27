import constants.StyleDefinitions as style_def_tags
import re


def escape_regex(exp):
    new_exp = re.sub(r"\s", "\\s", exp)
    print(new_exp)
    for c in style_def_tags.ESCAPE_CHAR_LIST:
        new_exp.replace(c, "\\{c}".format(c=c))
    return new_exp


# Escape the special characters in the tags used in this file because all the regExps will be escaped too
CI_TAG_START = escape_regex(style_def_tags.CI_TAG_START)
CI_TAG_END = escape_regex(style_def_tags.CI_TAG_END)
FIELD_TAG_START = escape_regex(style_def_tags.FIELD_TAG_START)
FIELD_TAG_END = escape_regex(style_def_tags.FIELD_TAG_END)
OPT_TAG_START = escape_regex(style_def_tags.OPT_TAG_START)
OPT_TAG_END = escape_regex(style_def_tags.OPT_TAG_END)
QUOTE_TAG_START = escape_regex(style_def_tags.QUOTE_TAG_START)
QUOTE_TAG_END = escape_regex(style_def_tags.QUOTE_TAG_END)


# If a regEx contains <ci>test<ci>, this function replaces it with [Tt][Ee][Ss][Tt]
# so that a case insensitive match can take place
def replace_ci_tags(exp):
    # Perform a re.sub() so that the ci_tag is replaced with the new text
    # The sub pattern is used for re.sub
    group_name = "ci_text"
    sub_pattern = "{start_tag}(?P<{group_name}>((?!{start_tag}|{end_tag}).)*){end_tag}".format(
        start_tag=re.escape(CI_TAG_START),
        end_tag=re.escape(CI_TAG_END),
        group_name=group_name
    )

    # This function is used to replace the text within <ci> tags with an equivalent regExp i.e. the new_text variable
    def replacer(match_obj):
        new_text = ""
        for char in match_obj.group(group_name):
            new_text += "[{}]".format(char.upper() + char.lower())
        return new_text

    exp = re.sub(sub_pattern, replacer, exp)    # replace <ci> tags and the text enclosed -> with the new_text

    # If there still are some <ci> tags, there was some missing corresponding tag or the order wasn't right
    # Else, all is well so we return the new expression
    if CI_TAG_START in exp or CI_TAG_END in exp:
        raise Exception("Error parsing <ci> tags. Please check that for each <ci> tag, there is a corresponding </ci>"
                        " tag, there aren't any nested tags, and that their order is correct")
    else:
        return exp


# If a regEx contains <f>Book Title</f>, this function replaces it with (?P<Book_Title>.+),
# so that the author can be identified if a match is successful
# The whitespace is replaced with a '_' character because Python variable names can't have whitespaces in between
def replace_field_tags(exp):
    group_name = "f_text"
    sub_pattern = "{start_tag}(?P<{group_name}>((?!{start_tag}|{end_tag}).)*){end_tag}".format(
        start_tag=re.escape(FIELD_TAG_START),
        end_tag=re.escape(FIELD_TAG_END),
        group_name=group_name
    )

    # This function is used to replace the text within <f> tags with the group name that will be used to represent
    # that field e.g. <f>Book Author</f> means the a group named Book_Author will be used in the RegExp
    def replacer(match_obj):
        field_group_name = match_obj.group(group_name)
        if field_group_name != re.escape(field_group_name):
            raise Exception("Error: only alphanumeric characters without spaces can be used as field names when"
                            " defining bibliography format")
        new_text = "(?P<{field_group_name}>.+)".format(
            field_group_name=field_group_name
        )
        return new_text

    new_exp = re.sub(sub_pattern, replacer, exp)    # replace <f> tags and the text enclosed -> with the new_text

    # If there still are some <f> tags, there was some missing corresponding tag or the order wasn't right
    # Else, all is well so we return the new expression
    if FIELD_TAG_START in new_exp or FIELD_TAG_END in new_exp:
        raise Exception("Error parsing <f> tags. Please check that for each <f> tag, there is a corresponding </f>"
                        " tag, there aren't any nested tags, and that their order is correct")
    else:
        return new_exp


# Replace optional tags with a regEx grouping such that the appearance of the enclosed text becomes optional
def replace_opt_tags(exp):
    new_exp = exp.replace(OPT_TAG_START, "(")
    new_exp = new_exp.replace(OPT_TAG_END, ")*")
    return new_exp


# Replace quote tags from the regEx so that the same quoting style (double vs single etc..) can be matched
def replace_quote_tags(exp):
    # new_exp = exp.replace(QUOTE_TAG_START, "(?P<quote>[\'\"])")
    # new_exp = new_exp.replace(QUOTE_TAG_END, "(?P=quote)")
    new_exp = exp.replace(QUOTE_TAG_START, "\"")
    new_exp = new_exp.replace(QUOTE_TAG_END, "\"")
    return new_exp