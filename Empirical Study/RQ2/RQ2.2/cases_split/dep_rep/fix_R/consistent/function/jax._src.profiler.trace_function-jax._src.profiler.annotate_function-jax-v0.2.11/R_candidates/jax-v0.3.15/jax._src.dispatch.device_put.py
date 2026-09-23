def device_put(x, device: Optional[Device] = None) -> Tuple[Any]:
  x = xla.canonicalize_dtype(x)
  try:
    return device_put_handlers[type(x)](x, device)
  except KeyError as err:
    raise TypeError(f"No device_put handler for type: {type(x)}") from err
