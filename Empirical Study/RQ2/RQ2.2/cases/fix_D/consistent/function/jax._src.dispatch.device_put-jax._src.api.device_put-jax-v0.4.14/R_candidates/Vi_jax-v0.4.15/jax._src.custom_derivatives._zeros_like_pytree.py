def _zeros_like_pytree(x):
  return tree_map(Zero.from_value, x)
