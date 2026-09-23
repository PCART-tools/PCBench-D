def nchw2nhwc(g, input):
    axes = [0, 2, 3, 1]
    return _permute_helper(g, input, axes)
