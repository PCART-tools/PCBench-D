@_onnx_symbolic("aten::isinf")
def isinf(g: jit_utils.GraphContext, input):
    return g.op("IsInf", g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.DOUBLE))
