@_onnx_symbolic("aten::neg")
def neg(g: jit_utils.GraphContext, self):
    return g.op("Neg", self)
