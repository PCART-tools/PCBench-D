@_onnx_symbolic("aten::acos")
def acos(g: jit_utils.GraphContext, self):
    return g.op("Acos", self)
