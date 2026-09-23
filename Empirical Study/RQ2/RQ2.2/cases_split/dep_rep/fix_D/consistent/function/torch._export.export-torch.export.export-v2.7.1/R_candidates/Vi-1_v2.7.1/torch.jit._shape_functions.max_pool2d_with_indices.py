def max_pool2d_with_indices(
    input: list[int],
    kernel_size: list[int],
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    ceil_mode: bool,
):
    out = max_pool2d(input, kernel_size, stride, padding, dilation, ceil_mode)
    return (out, out)
