@_onnx_symbolic("aten::rsub")
def rsub(g: jit_utils.GraphContext, self, other, alpha=None):
    return sub(g, other, self, alpha=alpha)
