@functools.partial(jnp.vectorize, signature='(n),(n)->(n)')
def _compose_quat(p: jax.Array, q: jax.Array) -> jax.Array:
  cross = jnp.cross(p[:3], q[:3])
  return jnp.array([p[3]*q[0] + q[3]*p[0] + cross[0],
                    p[3]*q[1] + q[3]*p[1] + cross[1],
                    p[3]*q[2] + q[3]*p[2] + cross[2],
                    p[3]*q[3] - p[0]*q[0] - p[1]*q[1] - p[2]*q[2]])
