@i0.defjvp
def _i0_jvp(primals, tangents):
  primal_out, tangent_out = jax.jvp(i0.fun, primals, tangents)
  return primal_out, where(primals[0] == 0, 0.0, tangent_out)
