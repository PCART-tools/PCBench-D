@_onnx_symbolic("aten::silu")
def silu(g: jit_utils.GraphContext, input):
    return g.op("Mul", input, g.op("Sigmoid", input))
