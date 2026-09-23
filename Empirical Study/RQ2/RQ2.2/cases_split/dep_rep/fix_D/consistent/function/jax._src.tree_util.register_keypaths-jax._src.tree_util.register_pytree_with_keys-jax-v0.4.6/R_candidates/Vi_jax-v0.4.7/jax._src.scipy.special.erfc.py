@_wraps(osp_special.erfc, module='scipy.special', update_doc=False)
def erfc(x: ArrayLike) -> Array:
  x, = promote_args_inexact("erfc", x)
  return lax.erfc(x)
