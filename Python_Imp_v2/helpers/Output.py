from constants.Configuration import OUTPUT_TAGGING_SYMBOL


def output_line_for_ref(groupdict, tag_dict, reftype_out_symbol):
    output_str = "{ts}{rt_tag}".format(ts=OUTPUT_TAGGING_SYMBOL, rt_tag=reftype_out_symbol)
    for key in groupdict.keys():
        field_tag = "{ts}{tag}".format(ts=OUTPUT_TAGGING_SYMBOL, tag=tag_dict[key])
        field_val = groupdict[key]
        field_str = "{ft} {fv}\n".format(ft=field_tag, fv=field_val)
        output_str += field_str
    output_str += "\n"
    return output_str
