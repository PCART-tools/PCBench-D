def conv3d(
    input: list[int],
    weight: list[int],
    bias: Optional[list[int]],
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    groups: int,
):
    assert len(weight) == 5
    assert len(input) == 5
    return conv_output_size(input, weight, bias, stride, padding, dilation, groups)
