@_wraps(np.full_like)
def full_like(a, fill_value, dtype=None, shape=None):
  lax_internal._check_user_dtype_supported(dtype, "full_like")
  _check_arraylike("full_like", a, fill_value)
  if shape is not None:
    shape = (shape,) if ndim(shape) == 0 else shape
  if ndim(fill_value) == 0:
    return lax.full_like(a, fill_value, dtype, shape)
  else:
    shape = np.shape(a) if shape is None else shape
    dtype = result_type(a) if dtype is None else dtype
    return broadcast_to(asarray(fill_value, dtype=dtype), shape)
