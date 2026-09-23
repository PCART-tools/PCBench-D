@partial(jit, static_argnames=('num', 'endpoint', 'dtype', 'axis'))
def _logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None,
             axis: int = 0):
  """Implementation of logspace differentiable in start and stop args."""
  lax_internal._check_user_dtype_supported(dtype, "logspace")
  if dtype is None:
    dtype = dtypes._to_inexact_dtype(result_type(start, stop))
  dtype = _jnp_dtype(dtype)
  computation_dtype = dtypes._to_inexact_dtype(dtype)
  _check_arraylike("logspace", start, stop)
  start = asarray(start, dtype=computation_dtype)
  stop = asarray(stop, dtype=computation_dtype)
  lin = linspace(start, stop, num,
                 endpoint=endpoint, retstep=False, dtype=None, axis=axis)
  return lax.convert_element_type(power(base, lin), dtype)
