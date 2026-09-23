def _device_put_impl(
    x, device: Optional[Union[Device, jax.sharding.Sharding]] = None):
  try:
    aval = xla.abstractify(x)
  except TypeError as err:
    raise TypeError(
        f"Argument '{x}' of type {type(x)} is not a valid JAX type") from err

  if isinstance(device, Sharding):
    if not jax.config.jax_array:
      raise RuntimeError(
          "Please enable `jax_array` to use device_put with a `Sharding`. "
          "You can use jax.config.update('jax_array', True) or set JAX_ARRAY=1 "
          "environment variable or set the `jax_array` boolean flag to "
          "something true-like.")
    s = device
    if not s.is_fully_addressable:  # type: ignore
      raise ValueError(
          "device_put's second argument must be a Device or a Sharding which "
          f"represents addressable devices, but got {s}")

    _check_sharding(aval, s)

    if getattr(x, 'sharding', None) == s:
      return x
    # TODO(mattjj,yashkatariya,phawkins): more runtime fast resharding here?
    result_handler = pxla.global_aval_to_result_handler(aval, s, True, False)
    map_ = s.devices_indices_map(aval.shape)  # type: ignore
    return result_handler(pxla.shard_arg(x, list(map_), list(map_.values()), s))

  # Only `Device` exists below. `Sharding` instance is handled above.
  if isinstance(x, array.ArrayImpl):
    if not x.is_fully_addressable:
      raise ValueError(
          "device_put's first argument must be a fully addressable array, but "
          f"got value with devices {x.devices()}")
    if device is None:
      return x
    elif is_single_device_sharding(x.sharding):
      return _copy_array_to_device(x, device)

  if device_array.type_is_device_array(x):
    return _copy_device_array_to_device(x, device)

  return aval_to_result_handler(device, aval)(None, *device_put(x, device))
