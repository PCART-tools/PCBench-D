@util._wraps(np.full_like)
def full_like(a: Union[ArrayLike, DuckTypedArray],
              fill_value: ArrayLike, dtype: Optional[DTypeLike] = None,
              shape: Any = None) -> Array:
  if hasattr(a, 'dtype') and hasattr(a, 'shape'):  # support duck typing
    util.check_arraylike("full_like", 0, fill_value)
  else:
    util.check_arraylike("full_like", a, fill_value)
  dtypes.check_user_dtype_supported(dtype, "full_like")
  if shape is not None:
    shape = canonicalize_shape(shape)
  if ndim(fill_value) == 0:
    return lax.full_like(a, fill_value, dtype, shape)
  else:
    shape = np.shape(a) if shape is None else shape  # type: ignore[arg-type]
    dtype = result_type(a) if dtype is None else dtype  # type: ignore[arg-type]
    return broadcast_to(asarray(fill_value, dtype=dtype), shape)
