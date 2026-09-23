@_wraps(osp_stats.cauchy.sf, update_doc=False)
def sf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, = promote_args_inexact("cauchy.sf", x)
  cdf_result = cdf(x, loc, scale)
  return lax.sub(_lax_const(cdf_result, 1), cdf_result)
