@_wraps(osp_special.gammaincc, module='scipy.special', update_doc=False)
def gammaincc(a, x):
  a, x = _promote_args_inexact("gammaincc", a, x)
  return lax.igammac(a, x)
