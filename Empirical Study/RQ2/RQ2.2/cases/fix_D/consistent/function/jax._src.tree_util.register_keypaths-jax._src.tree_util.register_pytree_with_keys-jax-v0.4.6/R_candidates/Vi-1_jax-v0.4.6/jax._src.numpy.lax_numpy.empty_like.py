@util._wraps(np.empty_like, lax_description="""\
Because XLA cannot create uninitialized arrays, the JAX version will
return an array initialized with zeros.""")
def empty_like(prototype: ArrayLike, dtype: Optional[DTypeLike] = None,
               shape: Any = None) -> Array:
  util._check_arraylike("empty_like", prototype)
  dtypes.check_user_dtype_supported(dtype, "empty_like")
  return zeros_like(prototype, dtype=dtype, shape=shape)
