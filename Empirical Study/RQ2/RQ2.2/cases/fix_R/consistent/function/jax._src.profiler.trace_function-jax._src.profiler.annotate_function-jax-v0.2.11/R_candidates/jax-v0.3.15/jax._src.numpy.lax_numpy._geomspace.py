@partial(jit, static_argnames=('num', 'endpoint', 'dtype', 'axis'))
def _geomspace(start, stop, num=50, endpoint=True, dtype=None, axis: int = 0):
  """Implementation of geomspace differentiable in start and stop args."""
  lax_internal._check_user_dtype_supported(dtype, "geomspace")
  if dtype is None:
    dtype = dtypes._to_inexact_dtype(result_type(start, stop))
  dtype = _jnp_dtype(dtype)
  computation_dtype = dtypes._to_inexact_dtype(dtype)
  _check_arraylike("geomspace", start, stop)
  start = asarray(start, dtype=computation_dtype)
  stop = asarray(stop, dtype=computation_dtype)
  # follow the numpy geomspace convention for negative and complex endpoints
  signflip = 1 - (1 - sign(real(start))) * (1 - sign(real(stop))) // 2
  signflip = signflip.astype(computation_dtype)
  res = signflip * logspace(log10(signflip * start),
                            log10(signflip * stop), num,
                            endpoint=endpoint, base=10.0,
                            dtype=computation_dtype, axis=0)
  if axis != 0:
    res = moveaxis(res, 0, axis)
  return lax.convert_element_type(res, dtype)
