@_wraps(np.full)
def full(shape, fill_value, dtype=None):
  lax_internal._check_user_dtype_supported(dtype, "full")
  _check_arraylike("full", fill_value)
  if ndim(fill_value) == 0:
    shape = (shape,) if ndim(shape) == 0 else shape
    return lax.full(shape, fill_value, dtype)
  else:
    return broadcast_to(asarray(fill_value, dtype=dtype), shape)
