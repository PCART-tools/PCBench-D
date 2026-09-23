@_wraps(osp_stats.cauchy.logpdf, update_doc=False)
def logpdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = _promote_args_inexact("cauchy.logpdf", x, loc, scale)
  pi = _lax_const(x, np.pi)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  normalize_term = lax.log(lax.mul(pi, scale))
  return lax.neg(lax.add(normalize_term, lax.log1p(lax.mul(scaled_x, scaled_x))))
