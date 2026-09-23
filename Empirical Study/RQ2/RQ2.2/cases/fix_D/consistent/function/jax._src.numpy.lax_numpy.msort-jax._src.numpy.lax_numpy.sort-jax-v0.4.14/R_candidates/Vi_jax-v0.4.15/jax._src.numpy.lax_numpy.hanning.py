@util._wraps(np.hanning)
def hanning(M: int) -> Array:
  M = core.concrete_or_error(int, M, "M argument of jnp.hanning")
  dtype = dtypes.canonicalize_dtype(float_)
  if M <= 1:
    return ones(M, dtype)
  n = lax.iota(dtype, M)
  return 0.5 * (1 - ufuncs.cos(2 * pi * n / (M - 1)))
