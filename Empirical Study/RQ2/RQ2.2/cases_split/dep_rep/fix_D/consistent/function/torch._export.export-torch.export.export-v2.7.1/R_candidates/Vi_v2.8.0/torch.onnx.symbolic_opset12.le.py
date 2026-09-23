@_onnx_symbolic("aten::le")
def le(g: jit_utils.GraphContext, input, other):
    return g.op("LessOrEqual", input, other)
