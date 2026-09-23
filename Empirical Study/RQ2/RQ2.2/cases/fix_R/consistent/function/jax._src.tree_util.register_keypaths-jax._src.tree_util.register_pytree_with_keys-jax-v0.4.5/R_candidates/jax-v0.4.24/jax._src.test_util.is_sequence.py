def is_sequence(x):
  try:
    iter(x)
  except TypeError:
    return False
  else:
    return True
