@util._wraps(np.zeros_like)
def zeros_like(a: ArrayLike, dtype: Optional[DTypeLike] = None,
               shape: Any = None) -> Array:
  util._check_arraylike("zeros_like", a)
  dtypes.check_user_dtype_supported(dtype, "zeros_like")
  if shape is not None:
    shape = canonicalize_shape(shape)
  return lax.full_like(a, 0, dtype, shape)
