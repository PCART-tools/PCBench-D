@_onnx_symbolic("aten::isfinite")
def isfinite(g: jit_utils.GraphContext, input):
    inf_node = isinf(g, input)
    nan_node = opset9.isnan(g, input)
    return opset9.__not_(g, opset9.__or_(g, inf_node, nan_node))
