@_wraps(osp_stats.gamma.logpdf, update_doc=False)
def logpdf(x, a, loc=0, scale=1):
  x, a, loc, scale = _promote_args_inexact("gamma.logpdf", x, a, loc, scale)
  one = _lax_const(x, 1)
  y = lax.div(lax.sub(x, loc), scale)
  log_linear_term = lax.sub(xlogy(lax.sub(a, one), y), y)
  shape_terms = lax.add(gammaln(a), lax.log(scale))
  log_probs = lax.sub(log_linear_term, shape_terms)
  return where(lax.lt(x, loc), -inf, log_probs)
