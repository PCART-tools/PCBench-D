@parse_args("v", "i", "i", "i")
def narrow(g, input, dim, start, length):
    return sym_help._slice_helper(g, input, axes=[dim], starts=[start], ends=[start + length])
