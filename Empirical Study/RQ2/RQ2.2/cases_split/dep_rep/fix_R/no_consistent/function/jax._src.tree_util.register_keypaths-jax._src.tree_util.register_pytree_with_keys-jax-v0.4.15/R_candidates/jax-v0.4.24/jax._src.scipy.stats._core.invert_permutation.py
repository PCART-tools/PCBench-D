def invert_permutation(i: Array) -> Array:
  """Helper function that inverts a permutation array."""
  return jnp.empty_like(i).at[i].set(jnp.arange(i.size, dtype=i.dtype))
