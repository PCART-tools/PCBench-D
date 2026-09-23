@_onnx_symbolic("aten::_cast_Char")
@deprecated("Avoid using this function and create a Cast node instead")
def _cast_Char(g: jit_utils.GraphContext, input, non_blocking):
    return g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.INT8)
