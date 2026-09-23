def _uniform_helper(
    shape: ShapeType,
    low: Union[bool, int, float] = 0.0,
    high: Union[bool, int, float] = 1.0,
    *,
    dtype: torch.dtype,
    device: DeviceLikeType,
) -> TensorLikeType:
    utils.validate_shape(shape)

    assert isinstance(low, Number)
    assert isinstance(high, Number)
    low = sym_float(low)
    high = sym_float(high)

    assert isinstance(dtype, torch.dtype)
    device = utils.canonicalize_device(device)

    return prims._uniform_helper(shape, low=low, high=high, dtype=dtype, device=device)
