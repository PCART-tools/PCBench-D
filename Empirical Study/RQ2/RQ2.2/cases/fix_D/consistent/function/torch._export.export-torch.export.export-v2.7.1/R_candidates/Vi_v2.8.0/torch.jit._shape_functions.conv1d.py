def conv1d(
    input: list[int],
    weight: list[int],
    bias: Optional[list[int]],
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    groups: int,
):
    assert len(weight) == 3
    assert len(input) == 3
    return conv_output_size(input, weight, bias, stride, padding, dilation, groups)
