def shard_sharded_device_array_slow_path(x, devices, indices, sharding):
  candidates = defaultdict(list)
  if isinstance(x, ArrayImpl):
    bufs = [buf.data for buf in x.addressable_shards]
    arr_indices = tuple(x.sharding.devices_indices_map(x.shape).values())
  else:
    bufs = x.device_buffers
    arr_indices = x.indices
  for buf, idx in safe_zip(bufs, arr_indices):
    candidates[_hashable_index(idx)].append(buf)

  bufs = []
  for idx, device in safe_zip(indices, devices):
    # Look up all buffers that contain the correct slice of the logical array.
    candidates_list = candidates[_hashable_index(idx)]
    if not candidates_list:
      # This array isn't sharded correctly. Reshard it via host roundtrip.
      # TODO(skye): more efficient reshard?
      return pxla.shard_arg(x._value, sharding, canonicalize=False)
    # Try to find a candidate buffer already on the correct device,
    # otherwise copy one of them.
    for buf in candidates_list:
      if buf.devices() == {device}:
        bufs.append(buf)
        break
    else:
      bufs.append(buf)

  return pxla.batched_device_put(x.aval, sharding, bufs, devices)
