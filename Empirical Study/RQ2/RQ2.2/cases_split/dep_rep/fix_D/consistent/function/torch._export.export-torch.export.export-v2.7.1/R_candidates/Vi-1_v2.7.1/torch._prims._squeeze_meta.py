def _squeeze_meta(a: TensorLikeType, dimensions: Sequence) -> TensorLikeType:
    assert isinstance(a, TensorLike)

    for idx in dimensions:
        utils.validate_idx(a.ndim, idx)
        assert a.shape[idx] == 1

    new_shape = []
    new_strides = []
    for idx in range(len(a.shape)):
        if idx in dimensions:
            continue

        new_shape.append(a.shape[idx])
        new_strides.append(a.stride()[idx])

    return a.as_strided(new_shape, new_strides, a.storage_offset())
