def _uninitialized_value(shape, dtype):
  if jnp.issubdtype(dtype, jnp.floating):
    return jnp.full(shape, jnp.nan, dtype)
  elif jnp.issubdtype(dtype, jnp.integer):
    return jnp.full(shape, jnp.iinfo(dtype).min, dtype)
  raise NotImplementedError(dtype)
