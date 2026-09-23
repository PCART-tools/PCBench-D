def backends() -> dict[str, xla_client.Client]:
  global _backends
  global _backend_errors
  global _default_backend
  global _plugins_registered

  # Needs a separate lock because register_backend_factory (called from
  # register_plugin) requries to hold _backend_lock.
  with _plugin_lock:
    if not _plugins_registered:
      # Plugins in the namespace package `jax_plugins` or have an entry-point
      # under the `jax_plugins` group will be imported.
      discover_pjrt_plugins()
      # Registers plugins names and paths set in env var
      # PJRT_NAMES_AND_LIBRARY_PATHS, in the format of 'name1:path1,name2:path2'
      # ('name1;path1,name2;path2' for windows).
      register_pjrt_plugin_factories_from_env()
      _plugins_registered = True

  with _backend_lock:
    if _backends:
      return _backends
    if jax_platforms := config.jax_platforms.value:
      platforms = []
      # Allow platform aliases in the list of platforms.
      for platform in jax_platforms.split(","):
        platforms.extend(expand_platform_alias(platform))
      priorities = range(len(platforms), 0, -1)
      # If the user specified a list of platforms explicitly, always fail
      # loudly.
      fail_quietly_list = [False] * len(platforms)
      platform_registrations = list(
        zip(platforms, priorities, fail_quietly_list))
    else:
      platform_registrations = [
          (platform, registration.priority, registration.fail_quietly)
          for platform, registration
          in _backend_factories.items()
      ]
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
          _backend_errors[platform] = str(err)
          logger.info(err_msg)
        else:
          if config.jax_platforms.value:
            err_msg += " (set JAX_PLATFORMS='' to automatically choose an available backend)"
          else:
            err_msg += " (you may need to uninstall the failing plugin package, or set JAX_PLATFORMS=cpu to skip this backend.)"
          raise RuntimeError(err_msg)

    assert _default_backend is not None
    if not config.jax_platforms.value:
      _suggest_missing_backends()
    return _backends
