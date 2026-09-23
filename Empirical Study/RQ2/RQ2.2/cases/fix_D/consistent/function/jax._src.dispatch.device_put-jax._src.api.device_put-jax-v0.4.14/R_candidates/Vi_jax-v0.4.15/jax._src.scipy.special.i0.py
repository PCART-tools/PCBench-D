@_wraps(osp_special.i0, module='scipy.special')
def i0(x: ArrayLike) -> Array:
  x, = promote_args_inexact("i0", x)
  return lax.mul(lax.exp(lax.abs(x)), lax.bessel_i0e(x))
