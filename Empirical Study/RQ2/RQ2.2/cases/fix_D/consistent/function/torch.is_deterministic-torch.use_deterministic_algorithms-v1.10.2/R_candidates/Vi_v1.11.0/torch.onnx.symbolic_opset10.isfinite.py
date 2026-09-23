def isfinite(g, input):
    from torch.onnx.symbolic_opset9 import isnan, __not_, __or_
    inf_node = isinf(g, input)
    nan_node = isnan(g, input)
    return __not_(g, __or_(g, inf_node, nan_node))
