@_wraps(osp_special.gammainc, module='scipy.special', update_doc=False)
def gammainc(a: ArrayLike, x: ArrayLike) -> Array:
  a, x = promote_args_inexact("gammainc", a, x)
  return lax.igamma(a, x)
