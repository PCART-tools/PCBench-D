@_wraps(np.empty, lax_description="""\
Because XLA cannot create uninitialized arrays, the JAX version will
return an array initialized with zeros.""")
def empty(shape, dtype=None):
  lax_internal._check_user_dtype_supported(dtype, "empty")
  return zeros(shape, dtype)
