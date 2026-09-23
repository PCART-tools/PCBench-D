@_wraps(osp_stats.pareto.logpdf, update_doc=False)
def logpdf(x, b, loc=0, scale=1):
  x, b, loc, scale = _promote_args_inexact("pareto.logpdf", x, b, loc, scale)
  one = _lax_const(x, 1)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  normalize_term = lax.log(lax.div(scale, b))
  log_probs = lax.neg(lax.add(normalize_term, lax.mul(lax.add(b, one), lax.log(scaled_x))))
  return where(lax.lt(x, lax.add(loc, scale)), -inf, log_probs)
