@broadcast_to_p.def_impl
def _broadcast_to_impl(a, *, shape):
  import jax.numpy as jnp
  return jnp.broadcast_to(a, shape)
