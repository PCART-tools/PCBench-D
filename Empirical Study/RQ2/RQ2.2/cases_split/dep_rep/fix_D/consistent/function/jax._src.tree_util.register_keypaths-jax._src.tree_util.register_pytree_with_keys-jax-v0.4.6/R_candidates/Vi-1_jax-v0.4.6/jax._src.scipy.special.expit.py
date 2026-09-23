@_wraps(osp_special.expit, module='scipy.special', update_doc=False)
def expit(x: ArrayLike) -> Array:
  x, = _promote_args_inexact("expit", x)
  return lax.logistic(x)
