@_wraps(osp_stats.chi2.sf, update_doc=False)
def sf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  cdf_result = cdf(x, df, loc, scale)
  return lax.sub(_lax_const(cdf_result, 1), cdf_result)
