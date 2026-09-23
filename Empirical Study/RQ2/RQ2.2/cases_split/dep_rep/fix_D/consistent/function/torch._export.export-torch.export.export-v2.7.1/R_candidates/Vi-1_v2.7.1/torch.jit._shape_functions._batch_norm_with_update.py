def _batch_norm_with_update(
    input: list[int],
    weight: Optional[list[int]],
    bias: Optional[list[int]],
    running_mean: Optional[list[int]],
    running_var: Optional[list[int]],
) -> tuple[list[int], list[int], list[int], list[int]]:
    _size = [input[1]]
    return _copy(input), _size, _size, [0]
