@_wraps(np.zeros)
def zeros(shape, dtype=None):
  if isinstance(shape, types.GeneratorType):
    raise TypeError("expected sequence object with len >= 0 or a single integer")
  lax_internal._check_user_dtype_supported(dtype, "zeros")
  shape = canonicalize_shape(shape)
  return lax.full(shape, 0, _jnp_dtype(dtype))
