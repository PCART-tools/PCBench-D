def _softmax(x, axis) -> Array:
  """Utility to compute the softmax of x along a given axis."""
  if not dtypes.issubdtype(x.dtype, np.floating):
    raise TypeError(f"_softmax only accepts floating dtypes, got {x.dtype}")
  x_max = jnp.max(x, axis, keepdims=True)
  unnormalized = jnp.exp(x - lax.stop_gradient(x_max))
  return unnormalized / unnormalized.sum(axis, keepdims=True)
