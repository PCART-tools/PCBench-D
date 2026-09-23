def max(g, self, dim_or_y=None, keepdim=None):
    # torch.max(input, other)
    if keepdim is None and dim_or_y is not None:
        warnings.warn("Multidirectional broadcasting is not supported in opset 7. "
                      "This might cause the onnx model to be incorrect, if inputs to max operators "
                      "have different shapes")
    return sym_opset9.max(g, self, dim_or_y, keepdim)
