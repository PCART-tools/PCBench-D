@_wraps(osp_special.i0e, module='scipy.special')
def i0e(x: ArrayLike) -> Array:
  x, = promote_args_inexact("i0e", x)
  return lax.bessel_i0e(x)
