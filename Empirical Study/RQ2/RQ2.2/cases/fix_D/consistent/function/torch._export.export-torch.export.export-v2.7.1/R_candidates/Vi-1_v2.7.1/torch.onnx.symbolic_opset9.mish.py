@_onnx_symbolic("aten::mish")
def mish(g: jit_utils.GraphContext, input):
    return g.op("Mul", input, g.op("Tanh", g.op("Softplus", input)))
