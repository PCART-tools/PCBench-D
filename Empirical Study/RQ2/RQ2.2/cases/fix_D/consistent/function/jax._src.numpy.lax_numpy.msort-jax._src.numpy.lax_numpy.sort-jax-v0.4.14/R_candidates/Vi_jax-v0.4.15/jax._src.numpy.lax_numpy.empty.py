@util._wraps(np.empty, lax_description="""\
Because XLA cannot create uninitialized arrays, the JAX version will
return an array initialized with zeros.""")
def empty(shape: Any, dtype: DTypeLike | None = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "empty")
  return zeros(shape, dtype)
