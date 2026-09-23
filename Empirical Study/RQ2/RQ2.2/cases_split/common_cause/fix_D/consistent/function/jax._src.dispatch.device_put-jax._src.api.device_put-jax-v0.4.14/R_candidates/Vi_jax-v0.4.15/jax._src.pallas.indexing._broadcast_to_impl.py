@broadcast_to_p.def_impl
def _broadcast_to_impl(a, *, shape):
  return jnp.broadcast_to(a, shape)
