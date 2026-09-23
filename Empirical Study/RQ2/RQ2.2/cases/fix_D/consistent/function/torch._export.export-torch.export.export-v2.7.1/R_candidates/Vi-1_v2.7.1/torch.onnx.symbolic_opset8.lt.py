@_onnx_symbolic("aten::lt")
def lt(g: jit_utils.GraphContext, input, other):
    return _comparison_operator(g, input, other, "Less")
