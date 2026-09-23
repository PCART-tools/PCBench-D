@_onnx_symbolic("aten::_log_softmax")
@symbolic_helper.parse_args("v", "i", "i")
def _log_softmax(g: jit_utils.GraphContext, input, dim, half_to_float):
    if (
        half_to_float
        and _type_utils.JitScalarType.from_value(
            input, _type_utils.JitScalarType.UNDEFINED
        )
        == _type_utils.JitScalarType.HALF
    ):
        input = g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    return log_softmax(g, input, dim)
