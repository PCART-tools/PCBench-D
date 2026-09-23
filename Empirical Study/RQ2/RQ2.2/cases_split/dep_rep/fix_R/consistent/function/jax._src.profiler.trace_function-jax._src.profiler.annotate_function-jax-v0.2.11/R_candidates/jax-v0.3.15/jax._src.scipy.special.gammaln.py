@_wraps(osp_special.gammaln, module='scipy.special')
def gammaln(x):
  x, = _promote_args_inexact("gammaln", x)
  return lax.lgamma(x)
