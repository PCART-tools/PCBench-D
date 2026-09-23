def _inspect_sharding_impl(value, *, callback):
  if not config.jax_array:
    raise NotImplementedError("`inspect_sharding` not implemented.")
  callback(value.sharding)
  return []
