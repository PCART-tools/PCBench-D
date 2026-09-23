def broadcast_to(a: jax.Array, shape: Tuple[int, ...]) -> jax.Array:
  if a.shape == shape:
    return a
  return broadcast_to_p.bind(a, shape=shape)
