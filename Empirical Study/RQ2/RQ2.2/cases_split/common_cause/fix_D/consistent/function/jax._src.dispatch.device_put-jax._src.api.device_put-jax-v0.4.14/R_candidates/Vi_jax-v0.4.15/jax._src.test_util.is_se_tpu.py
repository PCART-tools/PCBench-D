def is_se_tpu():
  return (
      is_cloud_tpu() and not xla_bridge.using_pjrt_c_api()
  ) or xla_bridge.get_backend().platform_version.startswith(
      'StreamExecutor TPU'
  )
