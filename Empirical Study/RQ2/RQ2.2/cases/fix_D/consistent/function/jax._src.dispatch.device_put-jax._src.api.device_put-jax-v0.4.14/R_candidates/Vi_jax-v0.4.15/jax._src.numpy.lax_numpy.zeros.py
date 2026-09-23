@util._wraps(np.zeros)
def zeros(shape: Any, dtype: DTypeLike | None = None) -> Array:
  if isinstance(shape, types.GeneratorType):
    raise TypeError("expected sequence object with len >= 0 or a single integer")
  dtypes.check_user_dtype_supported(dtype, "zeros")
  shape = canonicalize_shape(shape)
  return lax.full(shape, 0, _jnp_dtype(dtype))
