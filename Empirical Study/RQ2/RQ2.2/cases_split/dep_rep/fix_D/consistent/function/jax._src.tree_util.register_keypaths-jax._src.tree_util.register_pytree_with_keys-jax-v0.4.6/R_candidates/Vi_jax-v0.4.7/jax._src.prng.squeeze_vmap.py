def squeeze_vmap(f, left):
  def squeeze_vmap_f(x, y):
    if left:
      x = jnp.squeeze(x, axis=0)
      axes = (None, 0)
    else:
      y = jnp.squeeze(y, axis=0)
      axes = (0, None)
    return jax.vmap(f, in_axes=axes, out_axes=0)(x, y)
  return squeeze_vmap_f
