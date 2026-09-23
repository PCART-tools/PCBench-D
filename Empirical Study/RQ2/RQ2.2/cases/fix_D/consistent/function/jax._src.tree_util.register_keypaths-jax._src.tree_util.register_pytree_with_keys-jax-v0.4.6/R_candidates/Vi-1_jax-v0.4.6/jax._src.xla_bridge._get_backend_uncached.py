def _get_backend_uncached(platform=None):
  # TODO(mattjj,skyewm): remove this input polymorphism after we clean up how
  # 'backend' values are handled
  if not isinstance(platform, (type(None), str)):
    return platform

  platform = (platform or FLAGS.jax_xla_backend or FLAGS.jax_platform_name
              or None)

  bs = backends()
  if platform is not None:
    platform = canonicalize_platform(platform)
    backend = bs.get(platform, None)
    if backend is None:
      if platform in _backends_errors:
        raise RuntimeError(f"Backend '{platform}' failed to initialize: "
                           f"{_backends_errors[platform]}")
      raise RuntimeError(f"Unknown backend {platform}")
    return backend
  else:
    return _default_backend
