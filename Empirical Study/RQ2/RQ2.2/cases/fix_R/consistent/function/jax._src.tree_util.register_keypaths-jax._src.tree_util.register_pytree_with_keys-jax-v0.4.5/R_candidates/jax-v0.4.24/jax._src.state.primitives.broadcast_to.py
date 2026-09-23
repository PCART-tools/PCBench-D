def broadcast_to(a: Array, shape: tuple[int, ...]) -> Array:
  import jax.numpy as jnp
  a = jnp.asarray(a)
  if a.shape == shape:
    return a
  return broadcast_to_p.bind(a, shape=shape)
