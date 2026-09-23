@_onnx_symbolic("aten::alias")
def alias(g: jit_utils.GraphContext, self):
    return self
