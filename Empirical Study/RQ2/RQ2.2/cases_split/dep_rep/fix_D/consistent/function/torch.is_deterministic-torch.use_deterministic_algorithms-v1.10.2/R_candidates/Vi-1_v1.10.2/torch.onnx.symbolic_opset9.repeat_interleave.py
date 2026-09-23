def repeat_interleave(g, self, repeats, dim=None, output_size=None):
    input = self
    # if dim is None flatten
    # By default, use the flattened input array, and return a flat output array
    if sym_help._is_none(dim):
        input = sym_help._reshape_helper(g, self, g.op("Constant", value_t=torch.tensor([-1])))
        dim = 0
    else:
        dim = sym_help._maybe_get_scalar(dim)

    repeats_dim = sym_help._get_tensor_rank(repeats)
    repeats_sizes = sym_help._get_tensor_sizes(repeats)
    input_sizes = sym_help._get_tensor_sizes(input)
    if repeats_dim is None:
        raise RuntimeError("Unsupported: ONNX export of repeat_interleave for unknown "
                           "repeats rank.")
    if repeats_sizes is None:
        raise RuntimeError("Unsupported: ONNX export of repeat_interleave for unknown "
                           "repeats size.")
    if input_sizes is None:
        raise RuntimeError("Unsupported: ONNX export of repeat_interleave for unknown "
                           "input size.")

    input_sizes_temp = input_sizes.copy()
    for idx, input_size in enumerate(input_sizes):
        if input_size is None:
            input_sizes[idx], input_sizes_temp[idx] = 0, -1

    # Cases where repeats is an int or single value tensor
    if (repeats_dim == 0 or (repeats_dim == 1 and repeats_sizes[0] == 1)):
        if not sym_help._is_tensor(repeats):
            repeats = g.op("Constant", value_t=torch.LongTensor(repeats))
        if input_sizes[dim] == 0:
            return sym_help._onnx_opset_unsupported_detailed("repeat_interleave", 9, 13,
                                                             "Unsupported along dimension with unknown input size")
        else:
            reps = input_sizes[dim]
            repeats = expand(g, repeats, g.op("Constant", value_t=torch.tensor([reps])), None)

    # Cases where repeats is a 1 dim Tensor
    elif repeats_dim == 1:
        if input_sizes[dim] == 0:
            return sym_help._onnx_opset_unsupported_detailed("repeat_interleave", 9, 13,
                                                             "Unsupported along dimension with unknown input size")
        if repeats_sizes[0] is None:
            return sym_help._onnx_opset_unsupported_detailed("repeat_interleave", 9, 13,
                                                             "Unsupported for cases with dynamic repeats")
        assert repeats_sizes[0] == input_sizes[dim], "repeats must have the same size as input along dim"
        reps = repeats_sizes[0]
    else:
        raise RuntimeError("repeats must be 0-dim or 1-dim tensor")

    final_splits = list()
    r_splits = sym_help._repeat_interleave_split_helper(g, repeats, reps, 0)
    i_splits = sym_help._repeat_interleave_split_helper(g, input, reps, dim)
    input_sizes[dim], input_sizes_temp[dim] = -1, 1
    for idx, r_split in enumerate(r_splits):
        i_split = unsqueeze(g, i_splits[idx], dim + 1)
        r_concat = [g.op("Constant", value_t=torch.LongTensor(input_sizes_temp[:dim + 1])),
                    r_split,
                    g.op("Constant", value_t=torch.LongTensor(input_sizes_temp[dim + 1:]))]
        r_concat = g.op("Concat", *r_concat, axis_i=0)
        i_split = expand(g, i_split, r_concat, None)
        i_split = sym_help._reshape_helper(g, i_split, g.op("Constant", value_t=torch.LongTensor(input_sizes)), allowzero=0)
        final_splits.append(i_split)
    return g.op("Concat", *final_splits, axis_i=dim)
