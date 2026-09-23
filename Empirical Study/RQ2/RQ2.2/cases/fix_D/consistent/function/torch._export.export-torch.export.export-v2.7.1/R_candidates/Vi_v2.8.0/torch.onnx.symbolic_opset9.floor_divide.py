@_onnx_symbolic("aten::floor_divide")
def floor_divide(g: jit_utils.GraphContext, self, other):
    # Deprecated behavior, floor_divide actually truncates
    return _trunc_divide(g, self, other)
