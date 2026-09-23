def logpmf(k, n, a, b, loc=0):
  """JAX implementation of scipy.stats.betabinom.logpmf."""
  k, n, a, b, loc = _promote_args_inexact("betabinom.logpmf", k, n, a, b, loc)
  y = lax.sub(lax.floor(k), loc)
  one = _lax_const(y, 1)
  zero = _lax_const(y, 0)
  combiln = lax.neg(lax.add(lax.log1p(n), betaln(lax.add(lax.sub(n,y), one), lax.add(y,one))))
  beta_lns = lax.sub(betaln(lax.add(y,a), lax.add(lax.sub(n,y),b)), betaln(a,b))
  log_probs = lax.add(combiln, beta_lns)
  y_cond = logical_or(lax.lt(y, lax.neg(loc)), lax.gt(y, lax.sub(n, loc)))
  log_probs = where(y_cond, -inf, log_probs)
  n_a_b_cond = logical_or(logical_or(lax.lt(n, one), lax.lt(a, zero)), lax.lt(b, zero))
  return where(n_a_b_cond, nan, log_probs)
