def is_device_cuda():
  return xla_bridge.get_backend().platform_version.startswith('cuda')
