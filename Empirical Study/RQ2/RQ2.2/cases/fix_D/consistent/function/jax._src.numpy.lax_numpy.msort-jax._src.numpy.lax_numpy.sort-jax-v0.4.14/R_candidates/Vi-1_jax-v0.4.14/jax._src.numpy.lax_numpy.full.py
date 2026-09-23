@util._wraps(np.full)
def full(shape: Any, fill_value: ArrayLike,
         dtype: Optional[DTypeLike] = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "full")
  util.check_arraylike("full", fill_value)
  if ndim(fill_value) == 0:
    shape = canonicalize_shape(shape)
    return lax.full(shape, fill_value, dtype)
  else:
    return broadcast_to(asarray(fill_value, dtype=dtype), shape)
