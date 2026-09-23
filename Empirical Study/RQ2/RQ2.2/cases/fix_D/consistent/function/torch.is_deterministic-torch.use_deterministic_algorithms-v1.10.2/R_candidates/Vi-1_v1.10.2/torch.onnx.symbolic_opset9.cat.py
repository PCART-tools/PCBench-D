@parse_args("v", "i")
def cat(g, tensor_list, dim):
    tensors = sym_help._unpack_list(tensor_list)
    return g.op("Concat", *tensors, axis_i=dim)
