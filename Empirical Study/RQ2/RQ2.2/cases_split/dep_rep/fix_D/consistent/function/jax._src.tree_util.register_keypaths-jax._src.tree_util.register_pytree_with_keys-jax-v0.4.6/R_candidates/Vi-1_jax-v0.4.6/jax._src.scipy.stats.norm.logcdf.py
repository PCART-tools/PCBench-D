@_wraps(osp_stats.norm.logcdf, update_doc=False)
def logcdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = _promote_args_inexact("norm.logcdf", x, loc, scale)
  # Cast required because custom_jvp return type is broken.
  return cast(Array, special.log_ndtr(lax.div(lax.sub(x, loc), scale)))
