def _shard_array(x, sharding):
  indices = tuple(sharding.addressable_devices_indices_map(x.shape).values())
  devices = get_addressable_devices_for_shard_arg(sharding)
  if x.dtype == dtypes.float0:
    x = np.zeros(x.shape, dtype=np.dtype(bool))
  aval = api_util.shaped_abstractify(x)
  return batched_device_put(aval, sharding, [x[i] for i in indices], devices)
