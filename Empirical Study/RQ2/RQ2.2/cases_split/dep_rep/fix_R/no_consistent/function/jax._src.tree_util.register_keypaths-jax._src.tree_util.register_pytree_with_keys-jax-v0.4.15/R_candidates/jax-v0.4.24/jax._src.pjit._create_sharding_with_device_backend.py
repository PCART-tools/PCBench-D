def _create_sharding_with_device_backend(device, backend):
  if device is not None:
    assert backend is None
    out = SingleDeviceSharding(device)
  elif backend is not None:
    assert device is None
    out = SingleDeviceSharding(xb.get_backend(backend).local_devices()[0])
  return out
