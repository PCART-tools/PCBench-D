@_wraps(osp_stats.norm.logpdf, update_doc=False)
def logpdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = _promote_args_inexact("norm.logpdf", x, loc, scale)
  scale_sqrd = lax.square(scale)
  log_normalizer = lax.log(lax.mul(_lax_const(x, 2 * np.pi), scale_sqrd))
  quadratic = lax.div(lax.square(lax.sub(x, loc)), scale_sqrd)
  return lax.div(lax.add(log_normalizer, quadratic), _lax_const(x, -2))
