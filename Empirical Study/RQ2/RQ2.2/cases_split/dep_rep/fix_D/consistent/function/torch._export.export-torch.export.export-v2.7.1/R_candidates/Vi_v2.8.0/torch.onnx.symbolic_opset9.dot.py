@_onnx_symbolic("aten::dot")
def dot(g: jit_utils.GraphContext, self, other):
    return matmul(g, self, other)
