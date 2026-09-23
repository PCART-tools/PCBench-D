@_wraps(osp_stats.beta.sf, update_doc=False)
def sf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
        loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  cdf_result = cdf(x, a, b, loc, scale)
  return lax.sub(_lax_const(cdf_result, 1), cdf_result)
