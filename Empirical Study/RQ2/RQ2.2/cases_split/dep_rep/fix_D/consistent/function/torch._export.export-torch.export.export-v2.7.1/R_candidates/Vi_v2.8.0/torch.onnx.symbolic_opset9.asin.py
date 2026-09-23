@_onnx_symbolic("aten::asin")
def asin(g: jit_utils.GraphContext, self):
    return g.op("Asin", self)
