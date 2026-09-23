@_wraps(osp_special.i1, module='scipy.special')
def i1(x: ArrayLike) -> Array:
  x, = promote_args_inexact("i1", x)
  return lax.mul(lax.exp(lax.abs(x)), lax.bessel_i1e(x))
