def _get_backend_uncached(
    platform: Union[None, str, xla_client.Client] = None
) -> xla_client.Client:
  # TODO(mattjj,skyewm): remove this input polymorphism after we clean up how
  # 'backend' values are handled
  if platform is not None and not isinstance(platform, str):
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
    assert _default_backend is not None
    return _default_backend
