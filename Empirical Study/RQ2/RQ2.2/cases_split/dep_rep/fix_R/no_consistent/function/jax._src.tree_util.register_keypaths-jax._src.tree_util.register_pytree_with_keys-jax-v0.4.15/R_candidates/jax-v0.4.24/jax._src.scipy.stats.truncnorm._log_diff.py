def _log_diff(x, y):
  return logsumexp(
    jnp.array([x, y]),
    b=jnp.array([jnp.ones_like(x), -jnp.ones_like(y)]),
    axis=0
  )
