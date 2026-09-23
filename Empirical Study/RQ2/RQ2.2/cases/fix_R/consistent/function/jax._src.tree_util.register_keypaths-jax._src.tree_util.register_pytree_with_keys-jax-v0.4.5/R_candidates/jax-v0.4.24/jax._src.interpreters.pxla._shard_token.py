def _shard_token(x, sharding):
  devices = get_addressable_devices_for_shard_arg(sharding)
  indices = _get_replicated_slices(len(devices))
  zeros = np.zeros((), dtype=np.dtype(np.bool_))
  aval = api_util.shaped_abstractify(zeros)
  return batched_device_put(aval, sharding, [zeros for _ in indices], devices)
