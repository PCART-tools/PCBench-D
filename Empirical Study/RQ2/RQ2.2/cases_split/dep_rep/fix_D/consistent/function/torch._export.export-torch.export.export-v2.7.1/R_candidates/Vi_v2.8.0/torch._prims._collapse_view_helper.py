def _collapse_view_helper(
    a: TensorLikeType, start: int, end: int
) -> tuple[Optional[ShapeType], Optional[StrideType]]:
    assert isinstance(a, TensorLike)

    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    _validate_collapse_args(a, start, end)

    # Special-case for zero dimensional tensors
    if a.ndim == 0:
        shape = (1,)
        strides = (1,)
    else:
        shape = a.shape  # type: ignore[assignment]
        strides = a.stride()  # type: ignore[assignment]

    if a.ndim == 0 or (end == start):
        return shape, strides

    length = shape[end]
    stride = strides[end]
    for idx in range(end - 1, start - 1, -1):
        if guard_size_oblivious(shape[idx] == 0) or guard_size_oblivious(
            shape[idx + 1] == 0
        ):
            length = 0
            stride = 0
            break

        if guard_size_oblivious(shape[idx] == 1):
            continue

        length = length * shape[idx]
        if guard_size_oblivious(stride < strides[idx]):
            stride = stride
        else:
            stride = strides[idx]

        if (
            guard_size_oblivious(a.numel() > 0)
            and guard_size_oblivious(shape[idx + 1] != 1)
            and not guard_size_oblivious(
                strides[idx] == strides[idx + 1] * shape[idx + 1]
            )
        ):
            return None, None

    new_shape = shape[:start] + (length,) + shape[end + 1 :]
    new_strides = strides[:start] + (stride,) + strides[end + 1 :]

    # NOTE: when the input has no elements it's restrided as if it were contiguous
    if guard_size_oblivious(a.numel() == 0):
        new_strides = utils.make_contiguous_strides_for(new_shape)

    return new_shape, new_strides
