def valid_jaxtype(x) -> bool:
  try:
    concrete_aval(x)
  except TypeError:
    return False
  else:
    return True
