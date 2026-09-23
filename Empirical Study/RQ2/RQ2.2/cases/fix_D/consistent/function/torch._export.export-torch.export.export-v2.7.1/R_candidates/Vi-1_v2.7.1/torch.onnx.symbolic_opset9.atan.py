@_onnx_symbolic("aten::atan")
def atan(g: jit_utils.GraphContext, self):
    return g.op("Atan", self)
