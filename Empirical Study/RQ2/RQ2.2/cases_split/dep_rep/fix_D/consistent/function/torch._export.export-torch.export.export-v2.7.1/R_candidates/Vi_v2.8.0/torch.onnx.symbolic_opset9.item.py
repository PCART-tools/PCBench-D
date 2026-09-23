@_onnx_symbolic("aten::item")
def item(g: jit_utils.GraphContext, self):
    return self
