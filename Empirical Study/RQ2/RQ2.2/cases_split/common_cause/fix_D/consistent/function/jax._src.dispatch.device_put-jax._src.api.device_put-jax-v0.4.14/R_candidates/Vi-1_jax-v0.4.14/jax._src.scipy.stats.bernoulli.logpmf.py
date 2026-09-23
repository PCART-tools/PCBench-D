@_wraps(osp_stats.bernoulli.logpmf, update_doc=False)
def logpmf(k: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  k, p, loc = promote_args_inexact("bernoulli.logpmf", k, p, loc)
  zero = _lax_const(k, 0)
  one = _lax_const(k, 1)
  x = lax.sub(k, loc)
  log_probs = xlogy(x, p) + xlog1py(lax.sub(one, x), -p)
  return jnp.where(jnp.logical_or(lax.lt(x, zero), lax.gt(x, one)),
                  -jnp.inf, log_probs)
