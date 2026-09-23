@_wraps(osp_stats.truncnorm.logsf, update_doc=False)
def logsf(x, a, b, loc=0, scale=1):
  x, a, b, loc, scale = _promote_args_inexact("truncnorm.logsf", x, a, b, loc, scale)
  x, a, b = jnp.broadcast_arrays(x, a, b)
  x = lax.div(lax.sub(x, loc), scale)
  logsf = _log_gauss_mass(x, b) - _log_gauss_mass(a, b)
  logcdf = _log_gauss_mass(a, x) - _log_gauss_mass(a, b)

  logsf = jnp.select(
    # third condition: avoid catastrophic cancellation (from scipy)
    [x >= b, x <= a, logsf > -0.1, x > a],
    [-jnp.inf, 0, jnp.log1p(-jnp.exp(logcdf)), logsf]
  )
  logsf = jnp.where(a >= b, jnp.nan, logsf)
  return logsf
