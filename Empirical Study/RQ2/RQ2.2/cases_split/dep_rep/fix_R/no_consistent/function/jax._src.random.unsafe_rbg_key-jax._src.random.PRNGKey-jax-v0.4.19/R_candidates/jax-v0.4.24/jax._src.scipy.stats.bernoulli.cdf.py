@implements(osp_stats.bernoulli.cdf, update_doc=False)
def cdf(k: ArrayLike, p: ArrayLike) -> Array:
  k, p = promote_args_inexact('bernoulli.cdf', k, p)
  zero, one = _lax_const(k, 0), _lax_const(k, 1)
  conds = [
    jnp.isnan(k) | jnp.isnan(p) | (p < zero) | (p > one),
    lax.lt(k, zero),
    jnp.logical_and(lax.ge(k, zero), lax.lt(k, one)),
    lax.ge(k, one)
    ]
  vals = [jnp.nan, zero, one - p, one]
  return jnp.select(conds, vals)
