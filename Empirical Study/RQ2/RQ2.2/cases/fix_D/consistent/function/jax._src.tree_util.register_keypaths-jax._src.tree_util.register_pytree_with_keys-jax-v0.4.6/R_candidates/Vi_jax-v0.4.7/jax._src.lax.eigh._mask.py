def _mask(x, dims, alternative=0):
  """Masks `x` up to the dynamic shape `dims`.

  Replaces values outside those dimensions with `alternative`. `alternative` is
  broadcast with `x`.
  """
  assert jnp.ndim(x) == len(dims)
  mask = None
  for i, d in enumerate(dims):
    if d is not None:
      mask_dim_i = lax.broadcasted_iota(jnp.int32, x.shape, i) < d
      mask = mask_dim_i if mask is None else (mask & mask_dim_i)
  return x if mask is None else jnp.where(mask, x, alternative)
