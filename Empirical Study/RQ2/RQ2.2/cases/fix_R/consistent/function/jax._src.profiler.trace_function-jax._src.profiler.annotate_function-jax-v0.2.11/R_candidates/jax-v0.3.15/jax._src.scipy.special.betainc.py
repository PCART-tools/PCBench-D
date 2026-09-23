@_wraps(osp_special.betainc, module='scipy.special')
def betainc(a, b, x):
  a, b, x = _promote_args_inexact("betainc", a, b, x)
  return lax.betainc(a, b, x)
