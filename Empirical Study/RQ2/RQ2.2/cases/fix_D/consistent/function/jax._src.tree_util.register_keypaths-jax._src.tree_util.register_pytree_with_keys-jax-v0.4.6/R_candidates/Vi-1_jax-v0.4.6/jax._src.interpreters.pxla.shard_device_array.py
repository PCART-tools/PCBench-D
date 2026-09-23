def shard_device_array(x, devices, indices, sharding):
  start_indices, limit_indices, removed_dims = unzip3(
      as_slice_indices(x, idx) for idx in indices)
  shards = x._multi_slice(start_indices, limit_indices, removed_dims)
  if jax.config.jax_array:
    aval = api_util.shaped_abstractify(x)
    return batched_device_put(aval, sharding, shards, devices)
  return device_put(shards, devices)
