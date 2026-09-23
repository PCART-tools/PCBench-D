@_wraps(osp_stats.gamma.logpdf, update_doc=False)
def logpdf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, a, loc, scale = promote_args_inexact("gamma.logpdf", x, a, loc, scale)
  one = _lax_const(x, 1)
  y = lax.div(lax.sub(x, loc), scale)
  log_linear_term = lax.sub(xlogy(lax.sub(a, one), y), y)
  shape_terms = lax.add(gammaln(a), lax.log(scale))
  log_probs = lax.sub(log_linear_term, shape_terms)
  return jnp.where(lax.lt(x, loc), -jnp.inf, log_probs)
