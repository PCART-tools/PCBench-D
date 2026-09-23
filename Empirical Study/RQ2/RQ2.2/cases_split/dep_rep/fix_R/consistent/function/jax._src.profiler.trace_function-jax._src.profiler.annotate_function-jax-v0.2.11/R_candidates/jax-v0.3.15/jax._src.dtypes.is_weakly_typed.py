def is_weakly_typed(x):
  try:
    return x.aval.weak_type
  except AttributeError:
    return type(x) in _weak_types
