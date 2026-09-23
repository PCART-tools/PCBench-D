def _all_gather_into_tensor_out_native_meta(input, group_size, group_name, *, out):
    shape = list(input.size())
    shape[0] *= group_size
    return input.new_empty(shape)
