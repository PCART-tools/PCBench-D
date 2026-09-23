@util._wraps(np.asarray, lax_description=_ARRAY_DOC)
def asarray(a: Any, dtype: Optional[DTypeLike] = None, order: Optional[str] = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "asarray")
  dtype = dtypes.canonicalize_dtype(dtype) if dtype is not None else dtype
  return array(a, dtype=dtype, copy=False, order=order)  # type: ignore
