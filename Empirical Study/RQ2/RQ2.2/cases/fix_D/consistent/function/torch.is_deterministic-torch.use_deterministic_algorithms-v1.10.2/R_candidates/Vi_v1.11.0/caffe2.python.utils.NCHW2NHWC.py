def NCHW2NHWC(tensor):
    assert tensor.ndim >= 2
    return tensor.transpose((0,) + tuple(range(2, tensor.ndim)) + (1,))
