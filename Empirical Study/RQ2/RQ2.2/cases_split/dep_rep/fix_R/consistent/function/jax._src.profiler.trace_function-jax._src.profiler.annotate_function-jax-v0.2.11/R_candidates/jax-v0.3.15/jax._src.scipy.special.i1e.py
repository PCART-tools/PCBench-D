@_wraps(osp_special.i1e, module='scipy.special')
def i1e(x):
  x, = _promote_args_inexact("i1e", x)
  return lax.bessel_i1e(x)
