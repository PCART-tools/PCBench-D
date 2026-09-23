def make_pjrt_tpu_topology(topology_name='', **kwargs):
  if not xla_client.pjrt_plugin_loaded("tpu"):
    library_path = _get_tpu_library_path()
    if library_path is None:
      raise RuntimeError(
          "JAX TPU support not installed; cannot generate TPU topology. See"
          " https://github.com/google/jax#installation")
    xla_client.load_pjrt_plugin_dynamically("tpu", library_path)
  assert xla_client.pjrt_plugin_loaded("tpu")
  if not xla_client.pjrt_plugin_initialized("tpu"):
    xla_client.initialize_pjrt_plugin("tpu")
  return xla_client.make_tfrt_tpu_c_api_device_topology(
      topology_name, **kwargs
  )
