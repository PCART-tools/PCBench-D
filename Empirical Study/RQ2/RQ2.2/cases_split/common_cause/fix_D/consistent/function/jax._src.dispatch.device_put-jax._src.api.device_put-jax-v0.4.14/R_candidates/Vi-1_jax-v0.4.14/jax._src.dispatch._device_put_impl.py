def _device_put_impl(
    x,
    device: Device | Sharding | None = None,
    src: Device | Sharding | None = None):
  from jax._src import array
  try:
    aval = xla.abstractify(x)
  except TypeError as err:
    raise TypeError(
        f"Argument '{x}' of type {type(x)} is not a valid JAX type") from err

  if isinstance(device, Sharding):
    s = device
    _check_sharding(aval, s)
    if getattr(x, 'sharding', None) == s:
      return x
    if (not s.is_fully_addressable and  # type: ignore
        isinstance(x, array.ArrayImpl) and not x.is_fully_addressable):
      # This has to be XLACompatible because _mcjax_reshard will run a
      # XLA computation.
      assert isinstance(s, XLACompatibleSharding)
      return _mcjax_reshard(x, s)
    if not s.is_fully_addressable:  # type: ignore
      raise ValueError(
          "device_put's second argument must be a Device or a Sharding which "
          f"represents addressable devices, but got {s}")
    return _put_x(x, s, aval, True)

  # Only `Device` exists below. `Sharding` instance is handled above.
  if isinstance(x, array.ArrayImpl):
    if not x.is_fully_addressable:
      raise ValueError(
          "device_put's first argument must be a fully addressable array, but "
          f"got value with devices {x.devices()}")
    if device is None:
      return x
    elif is_single_device_sharding(x.sharding):
      return pxla.batched_device_put(aval, SingleDeviceSharding(device), [x],
                                     [device])

  sh = SingleDeviceSharding(pxla._get_default_device()
                            if device is None else device)
  return _put_x(x, sh, aval, device is not None)
