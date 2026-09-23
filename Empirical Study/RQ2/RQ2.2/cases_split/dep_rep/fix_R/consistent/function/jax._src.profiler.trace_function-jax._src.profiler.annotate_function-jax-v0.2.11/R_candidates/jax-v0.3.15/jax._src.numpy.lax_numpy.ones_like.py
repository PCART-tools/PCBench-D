@_wraps(np.ones_like)
def ones_like(a, dtype=None, shape=None):
  _check_arraylike("ones_like", a)
  lax_internal._check_user_dtype_supported(dtype, "ones_like")
  if np.isscalar(shape):
    shape = (shape,)
  return lax.full_like(a, 1, dtype, shape)
