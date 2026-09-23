@_wraps(osp_stats.norm.logcdf, update_doc=False)
def logcdf(x, loc=0, scale=1):
  x, loc, scale = _promote_args_inexact("norm.logcdf", x, loc, scale)
  return special.log_ndtr(lax.div(lax.sub(x, loc), scale))
