@util._wraps(np.zeros_like)
def zeros_like(a: ArrayLike | DuckTypedArray,
               dtype: DTypeLike | None = None,
               shape: Any = None) -> Array:
  if not (hasattr(a, 'dtype') and hasattr(a, 'shape')):  # support duck typing
    util.check_arraylike("ones_like", a)
  dtypes.check_user_dtype_supported(dtype, "zeros_like")
  if shape is not None:
    shape = canonicalize_shape(shape)
  return lax.full_like(a, 0, dtype, shape)
