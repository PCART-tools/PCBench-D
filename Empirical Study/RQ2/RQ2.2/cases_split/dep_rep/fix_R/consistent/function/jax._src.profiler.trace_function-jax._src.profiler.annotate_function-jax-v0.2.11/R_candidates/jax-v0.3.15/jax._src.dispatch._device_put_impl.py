def _device_put_impl(x, device: Optional[Device] = None):
  if device_array.type_is_device_array(x):
    return _copy_device_array_to_device(x, device)

  try:
    a = xla.abstractify(x)
  except TypeError as err:
    raise TypeError(
        f"Argument '{x}' of type {type(x)} is not a valid JAX type") from err
  return aval_to_result_handler(device, a)(None, *device_put(x, device))
