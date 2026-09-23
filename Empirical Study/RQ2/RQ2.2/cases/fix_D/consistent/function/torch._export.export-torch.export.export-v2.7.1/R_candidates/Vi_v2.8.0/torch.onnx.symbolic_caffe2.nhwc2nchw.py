def nhwc2nchw(g: jit_utils.GraphContext, input):
    axes = [0, 3, 1, 2]
    return _permute_helper(g, input, axes)
