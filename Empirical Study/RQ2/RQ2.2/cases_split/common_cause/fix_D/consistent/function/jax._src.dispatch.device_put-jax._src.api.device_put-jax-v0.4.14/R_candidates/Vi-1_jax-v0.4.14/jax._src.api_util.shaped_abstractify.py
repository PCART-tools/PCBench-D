def shaped_abstractify(x):
  try:
    return _shaped_abstractify_handlers[type(x)](x)
  except KeyError:
    return _shaped_abstractify_slow(x)
