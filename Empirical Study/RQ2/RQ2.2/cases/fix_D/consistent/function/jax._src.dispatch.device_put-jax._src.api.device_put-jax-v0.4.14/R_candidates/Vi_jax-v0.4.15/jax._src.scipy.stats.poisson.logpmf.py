@_wraps(osp_stats.poisson.logpmf, update_doc=False)
def logpmf(k: ArrayLike, mu: ArrayLike, loc: ArrayLike = 0) -> Array:
  k, mu, loc = promote_args_inexact("poisson.logpmf", k, mu, loc)
  zero = _lax_const(k, 0)
  x = lax.sub(k, loc)
  log_probs = xlogy(x, mu) - gammaln(x + 1) - mu
  return jnp.where(lax.lt(x, zero), -jnp.inf, log_probs)
