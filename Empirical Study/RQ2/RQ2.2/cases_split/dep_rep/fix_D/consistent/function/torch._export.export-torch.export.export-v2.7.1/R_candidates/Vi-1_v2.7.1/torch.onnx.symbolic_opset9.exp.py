@_onnx_symbolic("aten::exp")
def exp(g: jit_utils.GraphContext, self):
    return g.op("Exp", self)
