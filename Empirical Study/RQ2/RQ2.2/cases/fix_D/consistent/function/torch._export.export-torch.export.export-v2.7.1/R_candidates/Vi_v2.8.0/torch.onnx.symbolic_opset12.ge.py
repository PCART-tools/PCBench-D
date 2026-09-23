@_onnx_symbolic("aten::ge")
def ge(g: jit_utils.GraphContext, input, other):
    return g.op("GreaterOrEqual", input, other)
