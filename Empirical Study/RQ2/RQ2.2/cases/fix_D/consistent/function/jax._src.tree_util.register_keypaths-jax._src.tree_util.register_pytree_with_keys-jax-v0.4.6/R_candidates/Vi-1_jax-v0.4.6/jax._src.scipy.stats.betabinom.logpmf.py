@_wraps(osp_stats.betabinom.logpmf, update_doc=False)
def logpmf(k: ArrayLike, n: ArrayLike, a: ArrayLike, b: ArrayLike,
           loc: ArrayLike = 0) -> Array:
  """JAX implementation of scipy.stats.betabinom.logpmf."""
  k, n, a, b, loc = _promote_args_inexact("betabinom.logpmf", k, n, a, b, loc)
  y = lax.sub(lax.floor(k), loc)
  one = _lax_const(y, 1)
  zero = _lax_const(y, 0)
  combiln = lax.neg(lax.add(lax.log1p(n), betaln(lax.add(lax.sub(n,y), one), lax.add(y,one))))
  beta_lns = lax.sub(betaln(lax.add(y,a), lax.add(lax.sub(n,y),b)), betaln(a,b))
  log_probs = lax.add(combiln, beta_lns)
  y_cond = jnp.logical_or(lax.lt(y, lax.neg(loc)), lax.gt(y, lax.sub(n, loc)))
  log_probs = jnp.where(y_cond, -jnp.inf, log_probs)
  n_a_b_cond = jnp.logical_or(jnp.logical_or(lax.lt(n, one), lax.lt(a, zero)), lax.lt(b, zero))
  return jnp.where(n_a_b_cond, jnp.nan, log_probs)
