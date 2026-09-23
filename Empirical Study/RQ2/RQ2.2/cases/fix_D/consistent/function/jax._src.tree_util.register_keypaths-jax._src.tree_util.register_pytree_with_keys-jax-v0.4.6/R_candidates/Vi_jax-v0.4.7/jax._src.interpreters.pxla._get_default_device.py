def _get_default_device() -> xc.Device:
  return config.jax_default_device or xb.local_devices()[0]
