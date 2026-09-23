@_onnx_symbolic("aten::floor")
def floor(g: jit_utils.GraphContext, input):
    return g.op("Floor", input)
