@_wraps(np.i0)
@jit
def i0(x):
  x_orig = x
  x, = _promote_args_inexact("i0", x)
  if not issubdtype(x.dtype, np.floating):
    raise ValueError(f"Unsupported input type to jax.numpy.i0: {_dtype(x_orig)}")
  x = lax.abs(x)
  return lax.mul(lax.exp(x), lax.bessel_i0e(x))
