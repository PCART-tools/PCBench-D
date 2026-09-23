@_wraps(osp_stats.poisson.cdf, update_doc=False)
def cdf(k, mu, loc=0):
  k, mu, loc = jnp._promote_args_inexact("poisson.logpmf", k, mu, loc)
  zero = _lax_const(k, 0)
  x = lax.sub(k, loc)
  p = gammaincc(jnp.floor(1 + x), mu)
  return jnp.where(lax.lt(x, zero), zero, p)
