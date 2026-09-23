def nchw2nhwc(g: jit_utils.GraphContext, input):
    axes = [0, 2, 3, 1]
    return _permute_helper(g, input, axes)
