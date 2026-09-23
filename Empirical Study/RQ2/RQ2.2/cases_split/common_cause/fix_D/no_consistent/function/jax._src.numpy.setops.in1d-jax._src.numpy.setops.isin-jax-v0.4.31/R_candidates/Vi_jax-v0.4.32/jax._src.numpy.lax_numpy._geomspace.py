@partial(jit, static_argnames=('num', 'endpoint', 'dtype', 'axis'))
def _geomspace(start: ArrayLike, stop: ArrayLike, num: int = 50, endpoint: bool = True,
               dtype: DTypeLike | None = None, axis: int = 0) -> Array:
  """Implementation of geomspace differentiable in start and stop args."""
  dtypes.check_user_dtype_supported(dtype, "geomspace")
  if dtype is None:
    dtype = dtypes.to_inexact_dtype(result_type(start, stop))
  dtype = _jnp_dtype(dtype)
  computation_dtype = dtypes.to_inexact_dtype(dtype)
  util.check_arraylike("geomspace", start, stop)
  start = asarray(start, dtype=computation_dtype)
  stop = asarray(stop, dtype=computation_dtype)

  sign = ufuncs.sign(start)
  res = sign * logspace(ufuncs.log10(start / sign), ufuncs.log10(stop / sign),
                        num, endpoint=endpoint, base=10.0,
                        dtype=computation_dtype, axis=0)
  if axis != 0:
    res = moveaxis(res, 0, axis)
  return lax.convert_element_type(res, dtype)
