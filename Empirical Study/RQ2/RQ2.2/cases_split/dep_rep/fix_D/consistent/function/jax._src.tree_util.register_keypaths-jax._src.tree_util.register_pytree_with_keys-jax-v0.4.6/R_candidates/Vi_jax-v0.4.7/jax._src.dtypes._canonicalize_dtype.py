@functools.lru_cache(maxsize=None)
def _canonicalize_dtype(x64_enabled: bool, allow_opaque_dtype: bool, dtype: Any) -> Union[DType, OpaqueDType]:
  from jax._src import core     # TODO(frostig): break this cycle
  if core.is_opaque_dtype(dtype):
    if not allow_opaque_dtype:
      raise ValueError(f"Internal: canonicalize_dtype called onopaque dtype {dtype} "
                       "with allow_opaque_dtype=False")
    return dtype
  try:
    dtype_ = np.dtype(dtype)
  except TypeError as e:
    raise TypeError(f'dtype {dtype!r} not understood') from e

  if x64_enabled:
    return dtype_
  else:
    return _dtype_to_32bit_dtype.get(dtype_, dtype_)
