def _get_default_device() -> xc.Device:
  return config.default_device.value or xb.local_devices()[0]
