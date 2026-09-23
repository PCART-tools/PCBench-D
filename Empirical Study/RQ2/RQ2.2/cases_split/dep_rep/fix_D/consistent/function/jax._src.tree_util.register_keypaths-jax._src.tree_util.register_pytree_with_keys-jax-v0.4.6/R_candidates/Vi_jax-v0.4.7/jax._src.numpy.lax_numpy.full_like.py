@util._wraps(np.full_like)
def full_like(a: ArrayLike, fill_value: ArrayLike, dtype: Optional[DTypeLike] = None,
              shape: Any = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "full_like")
  util.check_arraylike("full_like", a, fill_value)
  if shape is not None:
    shape = canonicalize_shape(shape)
  if ndim(fill_value) == 0:
    return lax.full_like(a, fill_value, dtype, shape)
  else:
    shape = np.shape(a) if shape is None else shape
    dtype = result_type(a) if dtype is None else dtype
    return broadcast_to(asarray(fill_value, dtype=dtype), shape)
