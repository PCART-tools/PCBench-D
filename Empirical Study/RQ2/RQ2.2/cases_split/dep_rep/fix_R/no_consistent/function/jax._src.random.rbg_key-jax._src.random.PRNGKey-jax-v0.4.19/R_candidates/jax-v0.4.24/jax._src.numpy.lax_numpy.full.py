@util.implements(np.full)
def full(shape: Any, fill_value: ArrayLike,
         dtype: DTypeLike | None = None, *,
         device: xc.Device | Sharding | None = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "full")
  util.check_arraylike("full", fill_value)

  if ndim(fill_value) == 0:
    shape = canonicalize_shape(shape)
    return lax.full(shape, fill_value, dtype, sharding=_normalize_to_sharding(device))
  else:
    return _maybe_device_put(broadcast_to(asarray(fill_value, dtype=dtype), shape), device)
