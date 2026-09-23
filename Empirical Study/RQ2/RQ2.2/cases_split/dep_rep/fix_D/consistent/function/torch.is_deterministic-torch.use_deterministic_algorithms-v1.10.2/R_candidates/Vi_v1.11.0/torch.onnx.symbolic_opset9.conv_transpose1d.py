@parse_args("v", "v", "v", "is", "is", "is", "i", "is")
def conv_transpose1d(g, input, weight, bias, stride, padding, output_padding, groups, dilation):
    return _convolution(g, input, weight, bias, stride, padding, dilation, True, output_padding, groups, None, None, None, None)
