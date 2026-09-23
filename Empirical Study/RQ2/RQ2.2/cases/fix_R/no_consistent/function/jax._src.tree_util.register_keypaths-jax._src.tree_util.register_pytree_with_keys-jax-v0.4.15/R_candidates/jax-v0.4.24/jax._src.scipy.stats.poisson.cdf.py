@implements(osp_stats.poisson.cdf, update_doc=False)
def cdf(k: ArrayLike, mu: ArrayLike, loc: ArrayLike = 0) -> Array:
  k, mu, loc = promote_args_inexact("poisson.logpmf", k, mu, loc)
  zero = _lax_const(k, 0)
  x = lax.sub(k, loc)
  p = gammaincc(jnp.floor(1 + x), mu)
  return jnp.where(lax.lt(x, zero), zero, p)
