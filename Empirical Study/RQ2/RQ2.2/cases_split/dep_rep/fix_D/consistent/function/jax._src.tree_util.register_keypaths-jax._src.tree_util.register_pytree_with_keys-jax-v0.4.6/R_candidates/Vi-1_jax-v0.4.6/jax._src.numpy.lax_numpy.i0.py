@util._wraps(np.i0)
@jit
def i0(x: ArrayLike) -> Array:
  x_arr, = util._promote_args_inexact("i0", x)
  if not issubdtype(x_arr.dtype, np.floating):
    raise ValueError(f"Unsupported input type to jax.numpy.i0: {_dtype(x)}")
  x_arr = lax.abs(x_arr)
  return lax.mul(lax.exp(x_arr), lax.bessel_i0e(x_arr))
