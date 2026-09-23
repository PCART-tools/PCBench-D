@_onnx_symbolic("aten::gt")
def gt(g: jit_utils.GraphContext, input, other):
    return _comparison_operator(g, input, other, "Greater")
