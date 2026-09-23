@util._wraps(np.blackman)
def blackman(M: int) -> Array:
  M = core.concrete_or_error(int, M, "M argument of jnp.blackman")
  dtype = dtypes.canonicalize_dtype(float_)
  if M <= 1:
    return ones(M, dtype)
  n = lax.iota(dtype, M)
  return 0.42 - 0.5 * ufuncs.cos(2 * pi * n / (M - 1)) + 0.08 * ufuncs.cos(4 * pi * n / (M - 1))
