@util._wraps(np.ones)
def ones(shape: Any, dtype: DTypeLike | None = None) -> Array:
  if isinstance(shape, types.GeneratorType):
    raise TypeError("expected sequence object with len >= 0 or a single integer")
  shape = canonicalize_shape(shape)
  dtypes.check_user_dtype_supported(dtype, "ones")
  return lax.full(shape, 1, _jnp_dtype(dtype))
