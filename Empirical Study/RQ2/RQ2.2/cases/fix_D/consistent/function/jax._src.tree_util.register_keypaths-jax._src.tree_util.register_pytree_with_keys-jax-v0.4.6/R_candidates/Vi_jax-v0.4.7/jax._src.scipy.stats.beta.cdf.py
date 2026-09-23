@_wraps(osp_stats.beta.cdf, update_doc=False)
def cdf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
        loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, a, b, loc, scale = promote_args_inexact("beta.cdf", x, a, b, loc, scale)
  return betainc(
    a,
    b,
    lax.clamp(
      _lax_const(x, 0),
      lax.div(lax.sub(x, loc), scale),
      _lax_const(x, 1),
    )
  )
