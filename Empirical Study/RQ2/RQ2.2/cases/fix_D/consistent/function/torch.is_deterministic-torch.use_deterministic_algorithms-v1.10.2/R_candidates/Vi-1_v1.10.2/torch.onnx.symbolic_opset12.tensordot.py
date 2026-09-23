@parse_args("v", "v", "is", "is", "v")
def tensordot(g, input_a, input_b, dims_a, dims_b, out=None):
    if out is not None:
        _unimplemented("Tensordot", "Out parameter is not supported for tensordot.")

    dim_count_a = sym_help._get_tensor_rank(input_a)
    if dim_count_a is None:
        raise RuntimeError("Unsupported: ONNX export of tensordot for tensor(input_a) of unknown rank.")

    dim_count_b = sym_help._get_tensor_rank(input_b)
    if dim_count_b is None:
        raise RuntimeError("Unsupported: ONNX export of tensordot for tensor(input_b) of unknown rank.")

    dims_a = [(dims_a[i] + dim_count_a) if (dims_a[i] < 0) else dims_a[i] for i in range(len(dims_a))]
    dims_b = [(dims_b[i] + dim_count_b) if (dims_b[i] < 0) else dims_b[i] for i in range(len(dims_b))]

    left_dims_a = [i for i in range(dim_count_a) if (i not in dims_a)]
    left_dims_b = [i for i in range(dim_count_b) if (i not in dims_b)]

    new_input_a = permute(g, input_a, left_dims_a + dims_a)
    new_input_b = permute(g, input_b, dims_b + left_dims_b)

    input_shape = g.op("Shape", new_input_a)
    left_sizes_a = sym_help._slice_helper(g, input_shape, axes=[0], starts=[0], ends=[len(left_dims_a)])
    shape_sizes = [left_sizes_a, g.op("Constant", value_t=torch.tensor([-1], dtype=torch.long))]
    output_a = _reshape_from_tensor(g, new_input_a, shape_sizes)

    input_shape = g.op("Shape", output_a)
    slices = sym_help._slice_helper(g, input_shape, axes=[0], starts=[-1], ends=[maxsize])
    shape_sizes = [g.op("Constant", value_t=torch.tensor([-1], dtype=torch.long)), slices]
    output_a = _reshape_from_tensor(g, new_input_a, shape_sizes)

    input_shape = g.op("Shape", new_input_b)
    left_sizes_b = sym_help._slice_helper(g, input_shape, axes=[0], starts=[len(dims_b)], ends=[maxsize])
    slices = sym_help._slice_helper(g, input_shape, axes=[0], starts=[0], ends=[len(dims_b)])
    shape_sizes = [slices, g.op("Constant", value_t=torch.tensor([-1], dtype=torch.long))]
    output_b = _reshape_from_tensor(g, new_input_b, shape_sizes)

    input_shape = g.op("Shape", output_b)
    slices = sym_help._slice_helper(g, input_shape, axes=[0], starts=[-1], ends=[maxsize])
    shape_sizes = [g.op("Constant", value_t=torch.tensor([-1], dtype=torch.long)), slices]
    output_b = _reshape_from_tensor(g, new_input_b, shape_sizes)

    output = einsum(g, "ij,jk->ik", g.op("prim::ListConstruct", *[output_a, output_b]))

    shape_sizes = [left_sizes_a, left_sizes_b]
    return _reshape_from_tensor(g, output, shape_sizes)
