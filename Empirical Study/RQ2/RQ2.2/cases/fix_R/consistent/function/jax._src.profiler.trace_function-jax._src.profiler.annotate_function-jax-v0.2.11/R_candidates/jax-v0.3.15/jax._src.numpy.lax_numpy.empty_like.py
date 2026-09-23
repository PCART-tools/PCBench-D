@_wraps(np.empty_like, lax_description="""\
Because XLA cannot create uninitialized arrays, the JAX version will
return an array initialized with zeros.""")
def empty_like(prototype, dtype=None, shape=None):
  _check_arraylike("empty_like", prototype)
  lax_internal._check_user_dtype_supported(dtype, "empty_like")
  return zeros_like(prototype, dtype=dtype, shape=shape)
