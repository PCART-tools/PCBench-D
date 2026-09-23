def get_device_backend(
    device: Optional[xla_client.Device] = None,
) -> xla_client.Client:
  """Returns the Backend associated with `device`, or the default Backend."""
  if device is not None:
    return device.client
  return get_backend()
