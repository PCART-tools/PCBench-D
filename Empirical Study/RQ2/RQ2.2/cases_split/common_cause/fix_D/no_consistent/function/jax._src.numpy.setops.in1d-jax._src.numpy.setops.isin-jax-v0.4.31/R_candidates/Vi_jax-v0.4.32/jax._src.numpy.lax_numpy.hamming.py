@util.implements(np.hamming)
def hamming(M: int) -> Array:
  M = core.concrete_or_error(int, M, "M argument of jnp.hamming")
  dtype = dtypes.canonicalize_dtype(float_)
  if M <= 1:
    return ones(M, dtype)
  n = lax.iota(dtype, M)
  return 0.54 - 0.46 * ufuncs.cos(2 * pi * n / (M - 1))
