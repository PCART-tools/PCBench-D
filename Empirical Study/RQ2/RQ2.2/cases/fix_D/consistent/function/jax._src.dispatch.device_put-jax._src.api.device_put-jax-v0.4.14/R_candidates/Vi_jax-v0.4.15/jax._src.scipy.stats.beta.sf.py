@_wraps(osp_stats.beta.sf, update_doc=False)
def sf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
       loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, a, b, loc, scale = promote_args_inexact("beta.sf", x, a, b, loc, scale)
  return betainc(
    b,
    a,
    1 - lax.clamp(
      _lax_const(x, 0),
      lax.div(lax.sub(x, loc), scale),
      _lax_const(x, 1),
    )
  )
