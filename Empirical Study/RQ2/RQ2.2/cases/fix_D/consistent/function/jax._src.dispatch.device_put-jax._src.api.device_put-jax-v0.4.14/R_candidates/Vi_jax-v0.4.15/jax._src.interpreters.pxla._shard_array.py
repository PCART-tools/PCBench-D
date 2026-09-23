def _shard_array(x, devices, indices, sharding):
  if x.dtype == dtypes.float0:
    x = np.zeros(x.shape, dtype=np.dtype(bool))
  aval = api_util.shaped_abstractify(x)
  return batched_device_put(aval, sharding, [x[i] for i in indices], devices)
