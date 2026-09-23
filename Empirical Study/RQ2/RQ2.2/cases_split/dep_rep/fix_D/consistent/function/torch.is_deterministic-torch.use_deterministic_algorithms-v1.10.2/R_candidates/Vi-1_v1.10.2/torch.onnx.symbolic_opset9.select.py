@parse_args("v", "i", "v")
def select(g, self, dim, index):
    index = sym_help._maybe_get_scalar(index)
    if (not sym_help._is_value(index)) and (index < 0):
        if index == -1:
            end_index = 9223372036854775807
        else:
            end_index = index + 1
        slice_node = sym_help._slice_helper(g, self, axes=[dim], starts=[index], ends=[end_index])
        return sym_help._squeeze_helper(g, slice_node, [dim])
    else:
        return g.op("Gather", self, index, axis_i=dim)
