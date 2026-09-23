def prefetch(x):
  if isinstance(x, device_array.DeviceArray):
    x.copy_to_host_async()
  return x
