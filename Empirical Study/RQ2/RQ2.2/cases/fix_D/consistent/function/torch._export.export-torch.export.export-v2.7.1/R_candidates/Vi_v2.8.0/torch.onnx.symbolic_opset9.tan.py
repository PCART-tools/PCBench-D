@_onnx_symbolic("aten::tan")
def tan(g: jit_utils.GraphContext, self):
    return g.op("Tan", self)
