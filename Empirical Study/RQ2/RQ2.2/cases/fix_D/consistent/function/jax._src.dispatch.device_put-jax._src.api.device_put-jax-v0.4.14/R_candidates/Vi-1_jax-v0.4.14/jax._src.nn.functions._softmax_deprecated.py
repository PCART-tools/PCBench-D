def _softmax_deprecated(x, axis, where, initial):
  x_max = jnp.max(x, axis, where=where, initial=initial, keepdims=True)
  unnormalized = jnp.exp(x - lax.stop_gradient(x_max))
  result = unnormalized / jnp.sum(unnormalized, axis, where=where, keepdims=True)
  if where is not None:
    result = jnp.where(where, result, 0)
  return result
