def min(g, self, dim_or_y=None, keepdim=None):
    # torch.min(input, other)
    if keepdim is None and dim_or_y is not None:
        warnings.warn("Multidirectional broadcasting is not supported in opset 7. "
                      "This might cause the onnx model to be incorrect, if inputs to min operators "
                      "have different shapes")
    return sym_opset9.min(g, self, dim_or_y, keepdim)
