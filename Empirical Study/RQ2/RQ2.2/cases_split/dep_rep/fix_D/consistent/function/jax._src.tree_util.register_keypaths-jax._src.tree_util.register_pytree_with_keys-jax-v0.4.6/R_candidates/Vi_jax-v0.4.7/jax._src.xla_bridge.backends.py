def backends() -> Dict[str, xla_client.Client]:
  global _backends
  global _backends_errors
  global _default_backend

  with _backend_lock:
    if _backends:
      return _backends
    if config.jax_platforms:
      jax_platforms = config.jax_platforms.split(",")
      platforms = []
      # Allow platform aliases in the list of platforms.
      for platform in jax_platforms:
        platforms.extend(expand_platform_alias(platform))
      priorities = range(len(platforms), 0, -1)
      platforms_and_priorities = list(zip(platforms, priorities))
    else:
      platforms_and_priorities = list(
          (platform, priority) for platform, (_, priority)
          in _backend_factories.items())
    default_priority = -1000
    for platform, priority in platforms_and_priorities:
      try:
        backend = _init_backend(platform)
        _backends[platform] = backend

        if priority > default_priority:
          _default_backend = backend
          default_priority = priority
      except Exception as err:
        if platform in ('cpu', 'interpreter'):
          # We always expect the CPU and interpreter backends to initialize
          # successfully.
          raise
        else:
          # If the backend isn't built into the binary, or if it has no devices,
          # we expect a RuntimeError.
          err_msg = f"Unable to initialize backend '{platform}': {err}"
          if config.jax_platforms:
            err_msg += " (set JAX_PLATFORMS='' to automatically choose an available backend)"
            raise RuntimeError(err_msg)
          else:
            _backends_errors[platform] = str(err)
            logger.info(err_msg)
            continue
    assert _default_backend is not None
    # We don't warn about falling back to CPU on Mac OS, because we don't
    # support anything else there at the moment and warning would be pointless.
    if (py_platform.system() != "Darwin" and
        _default_backend.platform == "cpu" and
        FLAGS.jax_platform_name != 'cpu'):
      logger.warning('No GPU/TPU found, falling back to CPU. '
                      '(Set TF_CPP_MIN_LOG_LEVEL=0 and rerun for more info.)')
    return _backends
