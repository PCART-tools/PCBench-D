def _gda_shard_arg(x, devices, indices, sharding):
  x._check_if_deleted()
  return x._device_buffers
