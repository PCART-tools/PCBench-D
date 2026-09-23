def backends() -> dict[str, xla_client.Client]:
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
      # If the user specified a list of platforms explicitly, always fail
      # loudly.
      fail_quietly_list = [False] * len(platforms)
      platform_registrations = list(
        zip(platforms, priorities, fail_quietly_list))
    else:
      platform_registrations = list(
          (platform, registration.priority, registration.fail_quietly)
          for platform, registration
          in _backend_factories.items()
      )
    default_priority = -1000
    for platform, priority, fail_quietly in platform_registrations:
      try:
        backend = _init_backend(platform)
        _backends[platform] = backend

        if priority > default_priority:
          _default_backend = backend
          default_priority = priority
      except Exception as err:
        err_msg = f"Unable to initialize backend '{platform}': {err}"
        if fail_quietly:
          _backends_errors[platform] = str(err)
          logger.info(err_msg)
        else:
          if config.jax_platforms:
            err_msg += " (set JAX_PLATFORMS='' to automatically choose an available backend)"
          else:
            err_msg += " (you may need to uninstall the failing plugin package, or set JAX_PLATFORMS=cpu to skip this backend.)"
          raise RuntimeError(err_msg)

    assert _default_backend is not None
    # We don't warn about falling back to CPU on Mac OS, because we don't
    # support anything else there at the moment and warning would be pointless.
    if (py_platform.system() != "Darwin" and
        _default_backend.platform == "cpu" and
        _PLATFORM_NAME.value != 'cpu'):
      logger.warning('No GPU/TPU found, falling back to CPU. '
                      '(Set TF_CPP_MIN_LOG_LEVEL=0 and rerun for more info.)')
    return _backends
