@_onnx_symbolic("aten::cos")
def cos(g: jit_utils.GraphContext, self):
    return g.op("Cos", self)
