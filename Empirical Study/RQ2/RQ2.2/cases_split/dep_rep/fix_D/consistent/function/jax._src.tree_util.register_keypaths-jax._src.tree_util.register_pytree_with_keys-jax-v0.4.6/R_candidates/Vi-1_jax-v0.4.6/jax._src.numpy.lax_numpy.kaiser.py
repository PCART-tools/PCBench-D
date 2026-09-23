@util._wraps(np.kaiser)
def kaiser(M: int, beta: ArrayLike) -> Array:
  M = core.concrete_or_error(int, M, "M argument of jnp.kaiser")
  dtype = dtypes.canonicalize_dtype(float_)
  if M <= 1:
    return ones(M, dtype)
  n = lax.iota(dtype, M)
  alpha = 0.5 * (M - 1)
  return i0(beta * ufuncs.sqrt(1 - ((n - alpha) / alpha) ** 2)) / i0(beta)
