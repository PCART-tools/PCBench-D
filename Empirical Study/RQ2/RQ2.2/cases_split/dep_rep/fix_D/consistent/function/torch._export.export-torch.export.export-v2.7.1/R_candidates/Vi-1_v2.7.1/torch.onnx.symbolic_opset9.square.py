@_onnx_symbolic("aten::square")
def square(g: jit_utils.GraphContext, self):
    return g.op("Mul", self, self)
