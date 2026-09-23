def _collapse_view_meta(a: TensorLikeType, start: int, end: int) -> TensorLikeType:
    new_shape, new_strides = _collapse_view_helper(a, start, end)

    if new_shape is None:
        msg = "Attempting to view a collapsed tensor, but no such view exists!"
        raise ValueError(msg)

    assert new_strides is not None
    return a.as_strided(new_shape, new_strides, a.storage_offset())
