def _is_typeclass(a: Any) -> bool:
  try:
    return a in _type_classes
  except TypeError:
    return False
