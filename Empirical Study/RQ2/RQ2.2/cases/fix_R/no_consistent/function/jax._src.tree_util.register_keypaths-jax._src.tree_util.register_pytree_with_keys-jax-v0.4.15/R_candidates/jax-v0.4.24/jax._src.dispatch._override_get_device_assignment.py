def _override_get_device_assignment(sharding, *args, **kwargs):
  da = sharding._device_assignment
  return xb.get_device_backend(da[0]), da
