@_onnx_symbolic("aten::abs")
def abs(g: jit_utils.GraphContext, self):
    return g.op("Abs", self)
