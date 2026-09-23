@_onnx_symbolic("aten::log")
def log(g: jit_utils.GraphContext, self):
    return g.op("Log", self)
