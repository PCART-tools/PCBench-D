def check_valid_jaxtype(x):
  if not valid_jaxtype(x):
    raise TypeError(
      f"Value {x!r} of type {type(x)} is not a valid JAX type")
