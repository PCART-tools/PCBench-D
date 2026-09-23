@_onnx_symbolic("aten::logical_not")
def logical_not(g: jit_utils.GraphContext, input):
    return g.op("Not", g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.BOOL))
