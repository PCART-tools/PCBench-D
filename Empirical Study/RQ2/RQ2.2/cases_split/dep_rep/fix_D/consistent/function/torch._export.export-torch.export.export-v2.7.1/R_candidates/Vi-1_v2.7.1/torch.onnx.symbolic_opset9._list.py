@_onnx_symbolic("aten::list")
def _list(g: jit_utils.GraphContext, self):
    return self
