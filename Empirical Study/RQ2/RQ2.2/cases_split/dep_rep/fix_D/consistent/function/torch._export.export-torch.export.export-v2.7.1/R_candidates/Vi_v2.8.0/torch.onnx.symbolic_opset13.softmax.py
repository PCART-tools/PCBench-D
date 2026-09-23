@_onnx_symbolic("aten::softmax")
@symbolic_helper.parse_args("v", "i", "none")
def softmax(g: jit_utils.GraphContext, input, dim, dtype=None):
    softmax = g.op("Softmax", input, axis_i=dim)
    if dtype and dtype.node().kind() != "prim::Constant":
        parsed_dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        softmax = g.op(
            "Cast", softmax, to_i=_type_utils.JitScalarType(parsed_dtype).onnx_type()
        )

    return softmax
