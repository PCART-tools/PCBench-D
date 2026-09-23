def _shard_darray(x, devices, indices, sharding):
  return shard_arg(x._data, devices, indices, sharding)
