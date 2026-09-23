def arg_spec(x: Any) -> ArgSpec:
  aval = xla.abstractify(x)
  try:
    return aval, x._device
  except:
    return aval, None
