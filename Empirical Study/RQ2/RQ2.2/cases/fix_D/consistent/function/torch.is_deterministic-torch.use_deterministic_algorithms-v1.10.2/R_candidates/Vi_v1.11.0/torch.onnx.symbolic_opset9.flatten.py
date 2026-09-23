@parse_args("v", "i", "i")
def flatten(g, input, start_dim, end_dim):
    dim = sym_help._get_tensor_rank(input)
    if dim is None:
        return _unimplemented("dim",
                              "ONNX and PyTorch use different strategies to split the input. "
                              "Input rank must be known at export time.")

    # TODO: remove this as onnx opset 11 spec allows negative axes
    if end_dim < 0 :
        end_dim = dim + end_dim
    # use ONNX's Flatten operator for cases where the output shape is 2D
    if start_dim == 1 and end_dim == dim - 1 :
        return g.op("Flatten", input, axis_i=start_dim)
    if start_dim == 0 and end_dim == dim - 2 :
        return g.op("Flatten", input, axis_i=end_dim + 1)

    return sym_help._flatten_helper(g, input, start_dim, end_dim, dim)
