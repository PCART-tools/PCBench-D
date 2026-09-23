@_wraps(osp_stats.multinomial.logpmf, update_doc=False)
def logpmf(x: ArrayLike, n: ArrayLike, p: ArrayLike) -> Array:
  """JAX implementation of scipy.stats.multinomial.logpmf."""
  p, = promote_args_inexact("multinomial.logpmf", p)
  x, n = promote_args_numeric("multinomial.logpmf", x, n)
  if not jnp.issubdtype(x.dtype, jnp.integer):
    raise ValueError(f"x and n must be of integer type; got x.dtype={x.dtype}, n.dtype={n.dtype}")
  x = x.astype(p.dtype)
  n = n.astype(p.dtype)
  logprobs = gammaln(n + 1) + jnp.sum(xlogy(x, p) - gammaln(x + 1), axis=-1)
  return jnp.where(jnp.equal(jnp.sum(x), n), logprobs, -jnp.inf)
