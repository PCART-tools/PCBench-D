@_onnx_symbolic("aten::sign")
def sign(g: jit_utils.GraphContext, self):
    return g.op("Sign", self)
