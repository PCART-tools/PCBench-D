@functools.partial(jnp.vectorize, signature='(m)->(n)')
def _as_mrp(quat: jax.Array) -> jax.Array:
  sign = jnp.where(quat[3] < 0, -1., 1.)
  denominator = 1. + sign * quat[3]
  return sign * quat[:3] / denominator
