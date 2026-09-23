def _xla_callable_device(nreps, backend, device,
                         arg_devices) -> Optional[Device]:
  if nreps > 1:
    if device is not None or backend is not None:
      raise ValueError(f"can't specify device or backend for jit-of-pmap, "
                       f"got device={device} and backend={backend}")
    return None
  else:
    # TODO(skye): dedup with C++ jit logic for determining jit device?
    if device is not None:
      assert backend is None
      return device

    if backend is not None:
      return xb.get_backend(backend).get_default_device_assignment(1)[0]

    arg_device = _device_from_arg_devices(arg_devices)
    if arg_device is not None:
      return arg_device

    return config.jax_default_device
