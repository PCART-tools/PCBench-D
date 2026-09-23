@implements(osp_special.gammaincc, module='scipy.special', update_doc=False)
def gammaincc(a: ArrayLike, x: ArrayLike) -> Array:
  a, x = promote_args_inexact("gammaincc", a, x)
  return lax.igammac(a, x)
