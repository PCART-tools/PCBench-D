def definitely_equal(x, y):
  if isinstance(x, Tracer) or isinstance(y, Tracer):
    return same_referent(x, y)
  elif x is y:
    return True
  try:
    return x == y
  except InconclusiveDimensionOperation:
    return False
