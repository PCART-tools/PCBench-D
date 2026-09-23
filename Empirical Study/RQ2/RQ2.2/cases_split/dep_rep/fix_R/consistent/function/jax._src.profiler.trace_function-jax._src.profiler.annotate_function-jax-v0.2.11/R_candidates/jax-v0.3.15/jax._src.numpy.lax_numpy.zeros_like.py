@_wraps(np.zeros_like)
def zeros_like(a, dtype=None, shape=None):
  _check_arraylike("zeros_like", a)
  lax_internal._check_user_dtype_supported(dtype, "zeros_like")
  if np.isscalar(shape):
    shape = (shape,)
  return lax.full_like(a, 0, dtype, shape)
