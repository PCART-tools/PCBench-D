def _prepare_onnx_paddings(g, input, pad):
    if not sym_help._is_packed_list(pad) and sym_help._is_list(pad) and sym_help._is_scalar_list(pad):
        pad = g.op("ConcatFromSequence", pad, axis_i=0, new_axis_i=1)
    # The desired order of paddings is
    # dim_0_begin, dim_1_begin, ... , dim_0_end, ..., dim_n_end.
    # n is the dimension of input.
    # Assume zero-dimensions in the beginning, pad the "pad" sequence with zeros in the beginning
    pad_len = torch.onnx.symbolic_opset9.size(g, pad, g.op("Constant", value_t=torch.tensor([0])))
    # Set extension = [0] * (dim * 2 - len(pad))
    rank = sym_help._get_tensor_rank(input)
    if rank is None:
        rank = g.op("Size", g.op("Shape", input))
    else:
        rank = g.op("Constant", value_t=torch.tensor(rank, dtype=torch.int64))
    extension = g.op("Sub", g.op("Mul", rank,
                     g.op("Constant", value_t=torch.tensor(2, dtype=torch.int64))), pad_len)
    # Concat pad with extension: paddings = [dim_n_begin, dim_n_end, dim_n-1_begin, dim_n-1_end, 0, 0, ... ]
    # Currently ONNX only supports int64 type for Pad
    pad = g.op("Cast", pad, to_i=sym_help.cast_pytorch_to_onnx["Long"])
    paddings = g.op("Concat", pad, g.op("ConstantOfShape", extension, value_t=torch.tensor([0], dtype=torch.int64)), axis_i=0)
    # Reshape and reverse order and collate first beginnings and then ends
    # paddings = [[..., 0, dim_n-1_begin, dim_n_begin],
    #               [..., 0, dim_n-1_end, dim_n_end]]
    # Reshape back to 1-D paddings = [..., 0, dim_n - 1_begin, dim_n_begin, ..., 0, dim_n - 1_end, dim_n_end]
    paddings = sym_help._reshape_helper(g, paddings, g.op("Constant", value_t=torch.tensor([-1, 2])))
    paddings = g.op("Transpose", torch.onnx.symbolic_opset10.flip(g, paddings, [0]), perm_i=[1, 0])
    paddings = sym_help._reshape_helper(g, paddings, g.op("Constant", value_t=torch.tensor([-1])))
    padding_c = g.op("Cast", paddings, to_i=sym_help.cast_pytorch_to_onnx["Long"])
    return padding_c
