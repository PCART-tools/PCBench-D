@parse_args("s", "v")
def einsum(g, equation, tensor_list):
    tensors = sym_help._unpack_list(tensor_list)
    return einsum_helper(g, equation, tensors)
