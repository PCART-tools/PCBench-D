@_onnx_symbolic("aten::mv")
def mv(g: jit_utils.GraphContext, self, vec):
    return matmul(g, self, vec)
