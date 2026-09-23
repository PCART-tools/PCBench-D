def _stackable(*args: Any) -> bool:
  return all(type(arg) in stackables for arg in args)
