@parse_args("v", "i")
def stack(g, tensor_list, dim):
    unsqueezed = [sym_help._unsqueeze_helper(g, t, [dim]) for t in sym_help._unpack_list(tensor_list)]
    return g.op("Concat", *unsqueezed, axis_i=dim)
