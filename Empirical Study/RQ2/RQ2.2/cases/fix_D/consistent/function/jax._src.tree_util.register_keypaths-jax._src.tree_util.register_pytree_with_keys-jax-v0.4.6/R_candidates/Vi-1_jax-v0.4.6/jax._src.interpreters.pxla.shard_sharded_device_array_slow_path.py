def shard_sharded_device_array_slow_path(x, devices, indices, sharding):
  from jax._src.array import ArrayImpl

  candidates = defaultdict(list)
  if isinstance(x, ArrayImpl):
    bufs = x._arrays
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
      return shard_arg_handlers[type(x._value)](
          x._value, devices, indices, sharding)
    # Try to find a candidate buffer already on the correct device,
    # otherwise copy one of them.
    for buf in candidates_list:
      if buf.device() == device:
        bufs.append(buf)
        break
    else:
      bufs.append(buf.copy_to_device(device))
  if xla_extension_version >= 136 and isinstance(x, ArrayImpl):
    return ArrayImpl(x.aval, sharding, bufs, committed=True)
  return bufs
