@_onnx_symbolic("aten::log_softmax")
@symbolic_helper.parse_args("v", "i", "none")
def log_softmax(g: jit_utils.GraphContext, input, dim, dtype=None):
    return_op = g.op("LogSoftmax", input, axis_i=dim)
    if dtype and dtype.node().kind() != "prim::Constant":
        parsed_dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        return_op = g.op(
            "Cast", return_op, to_i=_type_utils.JitScalarType(parsed_dtype).onnx_type()
        )
    return return_op
