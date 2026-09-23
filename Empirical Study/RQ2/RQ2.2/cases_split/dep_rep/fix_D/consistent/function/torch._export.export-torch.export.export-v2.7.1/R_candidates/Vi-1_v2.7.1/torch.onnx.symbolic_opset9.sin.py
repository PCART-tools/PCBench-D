@_onnx_symbolic("aten::sin")
def sin(g: jit_utils.GraphContext, self):
    return g.op("Sin", self)
