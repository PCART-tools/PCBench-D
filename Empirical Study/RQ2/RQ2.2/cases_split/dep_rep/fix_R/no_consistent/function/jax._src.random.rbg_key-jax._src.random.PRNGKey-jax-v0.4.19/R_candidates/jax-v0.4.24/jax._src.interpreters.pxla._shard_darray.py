def _shard_darray(x, sharding):
  return shard_arg(x._data, sharding)
