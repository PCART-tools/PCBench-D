@partial(jit, static_argnames=('num', 'endpoint', 'dtype', 'axis'))
def _logspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
              endpoint: bool = True, base: ArrayLike = 10.0,
              dtype: Optional[DTypeLike] = None, axis: int = 0) -> Array:
  """Implementation of logspace differentiable in start and stop args."""
  dtypes.check_user_dtype_supported(dtype, "logspace")
  if dtype is None:
    dtype = dtypes.to_inexact_dtype(result_type(start, stop))
  dtype = _jnp_dtype(dtype)
  computation_dtype = dtypes.to_inexact_dtype(dtype)
  util.check_arraylike("logspace", start, stop)
  start = asarray(start, dtype=computation_dtype)
  stop = asarray(stop, dtype=computation_dtype)
  lin = linspace(start, stop, num,
                 endpoint=endpoint, retstep=False, dtype=None, axis=axis)
  return lax.convert_element_type(ufuncs.power(base, lin), dtype)
