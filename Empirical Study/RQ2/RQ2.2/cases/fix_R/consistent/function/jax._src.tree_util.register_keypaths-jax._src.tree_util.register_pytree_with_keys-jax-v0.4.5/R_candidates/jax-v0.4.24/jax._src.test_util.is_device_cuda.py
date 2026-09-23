def is_device_cuda():
  return 'cuda' in xla_bridge.get_backend().platform_version
