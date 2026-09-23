def conv2d(
    input: list[int],
    weight: list[int],
    bias: Optional[list[int]],
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    groups: int,
):
    assert len(weight) == 4
    assert len(input) == 4
    return conv_output_size(input, weight, bias, stride, padding, dilation, groups)
