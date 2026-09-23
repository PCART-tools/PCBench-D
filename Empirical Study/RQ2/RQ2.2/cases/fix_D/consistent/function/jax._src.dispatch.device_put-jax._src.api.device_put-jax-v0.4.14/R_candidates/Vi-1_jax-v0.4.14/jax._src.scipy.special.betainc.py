@_wraps(osp_special.betainc, module='scipy.special')
def betainc(a: ArrayLike, b: ArrayLike, x: ArrayLike) -> Array:
  a, b, x = promote_args_inexact("betainc", a, b, x)
  return lax.betainc(a, b, x)
