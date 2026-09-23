def dim(g, self):
    """Implement the dim functionality available for a pytorch tensor in ONNX"""
    # ONNX does not support dim directly in this opset so we can use 2 ops to get the info
    shape = g.op("Shape", self)
    return g.op("Size", shape)
