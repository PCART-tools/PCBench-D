def _valid_jaxtype(arg):
  try:
    xla.abstractify(arg)  # faster than core.get_aval
  except TypeError:
    return core.valid_jaxtype(arg)
  else:
    return True
