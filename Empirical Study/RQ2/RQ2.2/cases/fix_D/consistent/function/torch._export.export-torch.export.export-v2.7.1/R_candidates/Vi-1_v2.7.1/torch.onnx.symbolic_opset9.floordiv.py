@_onnx_symbolic("aten::floordiv")
def floordiv(g: jit_utils.GraphContext, self, other):
    return floor_divide(g, self, other)
