def _shard_token(x, devices, indices, sharding):
  zeros = np.zeros((), dtype=np.dtype(np.bool_))
  aval = api_util.shaped_abstractify(zeros)
  out = batched_device_put(aval, sharding, [zeros for i in indices], devices)
  return out
