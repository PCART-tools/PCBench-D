@util._wraps(np.asarray, lax_description=_ARRAY_DOC)
def asarray(a: Any, dtype: DTypeLike | None = None, order: str | None = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "asarray")
  if dtype is not None:
    dtype = dtypes.canonicalize_dtype(dtype, allow_extended_dtype=True)
  return array(a, dtype=dtype, copy=False, order=order)  # type: ignore
