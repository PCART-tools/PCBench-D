@_onnx_symbolic("aten::pow")
def pow(g: jit_utils.GraphContext, self, exponent):
    return g.op("Pow", self, exponent)
