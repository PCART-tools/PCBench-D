def _hash_accelerator_config(hash_obj, accelerators: np.ndarray, backend):
  accelerator_devices = []
  for accelerator in accelerators.flat:
    accelerator_devices.append(accelerator)
  try:
    hash_obj.update(
        xla_client.get_topology_for_devices(accelerator_devices).serialize()
    )
  except xla_client._xla.XlaRuntimeError as ex:
    # Fall back for those backends that do not support serialized
    # PjRtTopologyDescription as yet.
    logger.info("get (_hash_accelerator_config): unable to hash "
                "accelerator config, falling back to hashing "
                "devices + platform: %s (type %s)", ex, type(ex))
    _hash_devices(hash_obj, accelerators)
    _hash_platform(hash_obj, backend)
