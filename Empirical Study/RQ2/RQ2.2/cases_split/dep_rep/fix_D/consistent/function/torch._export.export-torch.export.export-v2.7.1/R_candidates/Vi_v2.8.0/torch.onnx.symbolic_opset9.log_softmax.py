@_onnx_symbolic("aten::log_softmax")
@symbolic_helper.parse_args("v", "i", "none")
def log_softmax(g: jit_utils.GraphContext, input, dim, dtype=None):
    # PyTorch dim and ONNX axis have different meanings.
    # See Softmax comment for details.
    # TODO: remove this as onnx opset 11 spec allows negative axes
    input_dim = symbolic_helper._get_tensor_rank(input)
    if input_dim is None:
        return symbolic_helper._unimplemented(
            "dim",
            "ONNX and PyTorch use different strategies to split the input. "
            "Input rank must be known at export time.",
        )
    if dim < 0:
        dim = input_dim + dim
    is_transpose_required = input_dim != dim + 1
    # ONNX only supports log_softmax with dim = -1. Transpose must be added before and after log_softmax to support other cases.
    if is_transpose_required:
        axes = list(range(input_dim))
        axes[dim], axes[-1] = axes[-1], axes[dim]
        input = g.op("Transpose", input, perm_i=axes)
        dim = input_dim - 1
    return_op = g.op("LogSoftmax", input, axis_i=dim)
    if dtype and dtype.node().kind() != "prim::Constant":
        parsed_dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        return_op = g.op(
            "Cast", return_op, to_i=_type_utils.JitScalarType(parsed_dtype).onnx_type()
        )
    if is_transpose_required:
        return_op = g.op("Transpose", return_op, perm_i=axes)  # type: ignore[possibly-undefined]
    return return_op
