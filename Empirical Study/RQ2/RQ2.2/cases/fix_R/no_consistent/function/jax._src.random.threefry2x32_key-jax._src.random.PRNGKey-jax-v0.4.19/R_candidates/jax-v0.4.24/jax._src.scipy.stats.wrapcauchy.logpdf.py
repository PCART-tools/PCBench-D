@implements(osp_stats.wrapcauchy.logpdf, update_doc=False)
def logpdf(x: ArrayLike, c: ArrayLike) -> Array:
  x, c = promote_args_inexact('wrapcauchy.logpdf', x, c)
  return jnp.where(
    lax.gt(c, _lax_const(c, 0)) & lax.lt(c, _lax_const(c, 1)),
    jnp.where(
      lax.ge(x, _lax_const(x, 0)) & lax.le(x, _lax_const(x, jnp.pi * 2)),
      jnp.log(1 - c * c) - jnp.log(2 * jnp.pi) - jnp.log(1 + c * c - 2 * c * jnp.cos(x)),
      -jnp.inf,
    ),
    jnp.nan,
  )
