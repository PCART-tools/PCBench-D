def _init_backend(platform):
  factory, unused_priority = _backend_factories.get(platform, (None, None))
  if factory is None:
    raise RuntimeError(f"Unknown backend '{platform}'")

  logger.debug("Initializing backend '%s'", platform)
  backend = factory()
  # TODO(skye): consider raising more descriptive errors directly from backend
  # factories instead of returning None.
  if backend is None:
    raise RuntimeError(f"Could not initialize backend '{platform}'")
  if backend.device_count() == 0:
    raise RuntimeError(f"Backend '{platform}' provides no devices.")
  util.distributed_debug_log(("Initialized backend", backend.platform),
                             ("process_index", backend.process_index()),
                             ("device_count", backend.device_count()),
                             ("local_devices", backend.local_devices()))
  logger.debug("Backend '%s' initialized", platform)
  return backend
