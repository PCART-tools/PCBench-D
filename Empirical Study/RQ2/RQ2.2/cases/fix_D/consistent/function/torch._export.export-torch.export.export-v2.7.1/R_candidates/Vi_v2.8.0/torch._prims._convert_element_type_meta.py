def _convert_element_type_meta(a: TensorLikeType, dtype: torch.dtype) -> TensorLikeType:
    # Type checks
    assert isinstance(a, TensorLike)
    assert isinstance(dtype, torch.dtype)

    # dtype conversion preserves dense strides
    if torch._prims_common.is_non_overlapping_and_dense(a):
        strides = a.stride()
    else:
        strides = utils.compute_elementwise_output_strides(a)

    return TensorMeta(a, strides=strides, dtype=dtype)
