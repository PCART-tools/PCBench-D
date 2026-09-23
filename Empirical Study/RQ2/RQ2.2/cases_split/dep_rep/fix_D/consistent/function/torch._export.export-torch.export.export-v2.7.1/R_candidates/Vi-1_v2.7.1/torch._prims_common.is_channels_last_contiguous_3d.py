def is_channels_last_contiguous_3d(a: Tensor) -> bool:
    # NDHWC or not channels last 3D contiguous
    if a.ndim != 5:
        return False

    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    expected_stride = 1
    for idx in (1, 4, 3, 2, 0):
        length = a.shape[idx]
        if guard_size_oblivious(length == 1):
            continue

        stride = a.stride()[idx]
        if guard_size_oblivious(stride != expected_stride):
            return False

        expected_stride *= length

    return True
