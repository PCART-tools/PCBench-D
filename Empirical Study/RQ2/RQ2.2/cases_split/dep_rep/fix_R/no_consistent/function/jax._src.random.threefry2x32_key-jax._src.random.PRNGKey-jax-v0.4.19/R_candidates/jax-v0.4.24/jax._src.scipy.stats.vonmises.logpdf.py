@implements(osp_stats.vonmises.logpdf, update_doc=False)
def logpdf(x: ArrayLike, kappa: ArrayLike) -> Array:
  x, kappa = promote_args_inexact('vonmises.logpdf', x, kappa)
  zero = _lax_const(kappa, 0)
  return jnp.where(lax.gt(kappa, zero), kappa * (jnp.cos(x) - 1) - jnp.log(2 * jnp.pi * lax.bessel_i0e(kappa)), jnp.nan)
