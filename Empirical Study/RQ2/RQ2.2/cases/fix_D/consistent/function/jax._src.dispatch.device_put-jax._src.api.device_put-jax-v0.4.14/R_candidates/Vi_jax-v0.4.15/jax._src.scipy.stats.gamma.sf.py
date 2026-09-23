@_wraps(osp_stats.gamma.sf, update_doc=False)
def sf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, a, loc, scale = promote_args_inexact("gamma.sf", x, a, loc, scale)
  return gammaincc(a, lax.div(lax.sub(x, loc), scale))
