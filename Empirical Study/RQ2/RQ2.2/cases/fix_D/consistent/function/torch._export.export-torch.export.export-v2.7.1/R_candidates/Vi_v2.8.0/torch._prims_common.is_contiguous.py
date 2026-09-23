def is_contiguous(a: TensorLikeType, false_if_dde=False) -> bool:
    """
    Tests whether a tensor is contiguous or not.

    Tensors are contiguous when they have no elements,
    one element, or when they have "nested" strides.
    """
    from torch.fx.experimental.symbolic_shapes import (
        guard_or_false,
        guard_or_true,
        guard_size_oblivious,
        is_nested_int,
    )

    maybe_guard_or_false = guard_or_false if false_if_dde else guard_size_oblivious
    maybe_guard_or_true = guard_or_true if false_if_dde else guard_size_oblivious

    if maybe_guard_or_false(a.numel() < 2):
        return True

    expected_stride = 1
    for x, y in reversed(tuple(zip(a.shape, a.stride()))):
        # Skips checking strides when a dimension has length 1.
        if maybe_guard_or_false(x == 1):
            continue

        if maybe_guard_or_true(y != expected_stride):
            return False

        # if x is 0 then a is contiguous anyway. So in the check above for non-contiguity condition we can
        # can assume x is not 0 in expected_stride equation. This make the check consistent with
        # make_contiguous_strides_for. If we make a tensor and used strides from make_contiguous_strides_for
        # and then called definitely_contiguous we should get True.
        expected_stride *= (
            x if is_nested_int(x) else sym_max(x, 1)
        )  # type:ignore[assignment]

    return True
