def check_shape_forward(
    input: list[int],
    weight_sizes: list[int],
    bias: Optional[list[int]],
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    groups: int,
):
    k = len(input)
    weight_dim = len(weight_sizes)

    # TODO: assertions could be expanded with the error messages
    assert not check_non_negative(padding)
    assert not check_non_negative(stride)

    assert weight_dim == k
    assert weight_sizes[0] >= groups
    assert (weight_sizes[0] % groups) == 0
    # only handling not transposed
    assert input[1] == weight_sizes[1] * groups
    assert bias is None or (len(bias) == 1 and bias[0] == weight_sizes[0])

    for i in range(2, k):
        assert (input[i] + 2 * padding[i - 2]) >= (
            dilation[i - 2] * (weight_sizes[i] - 1) + 1
        )
