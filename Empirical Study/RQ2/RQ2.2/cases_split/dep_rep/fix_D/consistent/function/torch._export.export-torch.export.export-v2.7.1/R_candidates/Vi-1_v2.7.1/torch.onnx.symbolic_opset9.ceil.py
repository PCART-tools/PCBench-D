@_onnx_symbolic("aten::ceil")
def ceil(g: jit_utils.GraphContext, input):
    return g.op("Ceil", input)
