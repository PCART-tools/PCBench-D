def shard_device_array(x, devices, indices, sharding):
  start_indices, limit_indices, removed_dims = unzip3(
      as_slice_indices(x, idx) for idx in indices)
  if sharding.is_fully_replicated:
    shards = [x] * len(devices)
  else:
    shards = x._multi_slice(start_indices, limit_indices, removed_dims)
  aval = api_util.shaped_abstractify(x)
  return pxla.batched_device_put(aval, sharding, shards, devices)
