def is_cloud_tpu():
  return 'libtpu' in xla_bridge.get_backend().platform_version
