@util.implements(np.bartlett)
def bartlett(M: int) -> Array:
  M = core.concrete_or_error(int, M, "M argument of jnp.bartlett")
  dtype = dtypes.canonicalize_dtype(float_)
  if M <= 1:
    return ones(M, dtype)
  n = lax.iota(dtype, M)
  return 1 - ufuncs.abs(2 * n + 1 - M) / (M - 1)
