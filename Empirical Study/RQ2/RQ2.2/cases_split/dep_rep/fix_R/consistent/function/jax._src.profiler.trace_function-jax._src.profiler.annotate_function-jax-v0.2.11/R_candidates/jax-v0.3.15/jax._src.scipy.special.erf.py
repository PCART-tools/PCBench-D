@_wraps(osp_special.erf, module='scipy.special')
def erf(x):
  x, = _promote_args_inexact("erf", x)
  return lax.erf(x)
