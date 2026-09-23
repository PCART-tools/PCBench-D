@parse_args("v", "v", "v", "is", "is", "is", "i")
def conv2d(g, input, weight, bias, stride, padding, dilation, groups):
    return _convolution(g, input, weight, bias, stride, padding, dilation, False, (), groups, None, None, None, None)
