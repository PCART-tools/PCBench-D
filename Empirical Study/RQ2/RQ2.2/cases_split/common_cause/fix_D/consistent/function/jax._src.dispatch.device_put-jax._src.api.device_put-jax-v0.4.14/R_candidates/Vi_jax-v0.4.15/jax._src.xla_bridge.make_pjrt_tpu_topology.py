def make_pjrt_tpu_topology(topology_name='', **kwargs):
  # TODO(b/261484192): Make a system for lazily loading libtpu.so and call
  # that inside make_tfrt_tpu_c_api_device_topology.
  get_backend()  # Properly initialize libtpu.so.
  return xla_client.make_tfrt_tpu_c_api_device_topology(
      topology_name, **kwargs
  )
