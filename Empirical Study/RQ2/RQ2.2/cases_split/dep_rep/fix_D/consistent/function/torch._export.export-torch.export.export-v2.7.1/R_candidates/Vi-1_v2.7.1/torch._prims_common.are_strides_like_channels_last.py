def are_strides_like_channels_last(
    shape: Sequence[int], strides: Sequence[int]
) -> bool:
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    ndim = len(shape)

    if ndim == 4:
        # Check for channels_last_2d
        dim_order = [1, 3, 2, 0]
    elif ndim == 5:
        # Check for channels_last_3d
        dim_order = [1, 4, 3, 2, 0]
    else:
        return False

    if guard_size_oblivious(strides[1] == 0):
        return False

    min = 0
    for d in dim_order:
        if guard_size_oblivious(shape[d] == 0):
            return False
        if guard_size_oblivious(strides[d] < min):
            return False
        if d == 0 and min == strides[1]:
            return False
        min = strides[d]
        if guard_size_oblivious(strides[d] > 1):
            min *= shape[d]
    return True
