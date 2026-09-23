def _array_shard_arg(x, devices, indices, sharding):
  x._check_if_deleted()

  x_indices = x.sharding.addressable_devices_indices_map(x.shape).values()
  if not x.is_fully_addressable:
    if tuple(x_indices) == tuple(indices):
      return x
    else:
      raise NotImplementedError(
          "Cannot reshard an input that is not fully addressable")
  else:
    if tuple(x_indices) == tuple(indices):
      return xc.copy_array_to_devices_with_sharding(
          x, list(devices), sharding)
    # Resharding starts here:
    if dispatch.is_single_device_sharding(x.sharding):
      return pxla.shard_device_array(x, devices, indices, sharding)
    else:
      return pxla.shard_sharded_device_array_slow_path(
          x, devices, indices, sharding)
