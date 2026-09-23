def NHWC2NCHW(tensor):
    assert tensor.ndim >= 1
    return tensor.transpose((0, tensor.ndim - 1) + tuple(range(1, tensor.ndim - 1)))
