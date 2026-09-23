def _conv_1d_output_size(size, kernel, pad, dilation, stride):
    return max(1, int((size + pad * 2 - (dilation * (kernel - 1) + 1)) / stride) + 1)
