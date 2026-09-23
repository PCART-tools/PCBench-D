def is_device_rocm():
  return xla_bridge.get_backend().platform_version.startswith('rocm')
