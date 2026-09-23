@_onnx_symbolic("aten::bmm")
def bmm(g: jit_utils.GraphContext, self, other):
    return g.op("MatMul", self, other)
