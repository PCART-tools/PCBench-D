@_wraps(osp_special.erfinv, module='scipy.special')
def erfinv(x):
  x, = _promote_args_inexact("erfinv", x)
  return lax.erf_inv(x)
