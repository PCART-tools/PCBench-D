@_wraps(osp_stats.bernoulli.ppf, update_doc=False)
def ppf(q: ArrayLike, p: ArrayLike) -> Array:
  q, p = _promote_args_inexact('bernoulli.ppf', q, p)
  zero, one = _lax_const(q, 0), _lax_const(q, 1)
  return jnp.where(
    jnp.isnan(q) | jnp.isnan(p) | (p < zero) | (p > one) | (q < zero) | (q > one),
    jnp.nan,
    jnp.where(lax.le(q, one - p), zero, one)
  )
