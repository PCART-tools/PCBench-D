def _clamp(min, operand, max):
  res = jnp.maximum(operand, min)
  return jnp.minimum(res, max)
