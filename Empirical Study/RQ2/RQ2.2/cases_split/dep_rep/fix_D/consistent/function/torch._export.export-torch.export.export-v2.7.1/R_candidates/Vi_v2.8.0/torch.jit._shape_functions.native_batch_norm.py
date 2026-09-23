def native_batch_norm(
    input: list[int],
    weight: Optional[list[int]],
    bias: Optional[list[int]],
    running_mean: Optional[list[int]],
    running_var: Optional[list[int]],
    training: bool,
) -> tuple[list[int], list[int], list[int]]:
    if training:
        _size = [input[1]]
    else:
        _size = [0]
    return _copy(input), _size, _size
