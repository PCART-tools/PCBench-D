def get_device_backend(device=None):
  """Returns the Backend associated with `device`, or the default Backend."""
  if device is not None:
    return device.client
  return get_backend()
