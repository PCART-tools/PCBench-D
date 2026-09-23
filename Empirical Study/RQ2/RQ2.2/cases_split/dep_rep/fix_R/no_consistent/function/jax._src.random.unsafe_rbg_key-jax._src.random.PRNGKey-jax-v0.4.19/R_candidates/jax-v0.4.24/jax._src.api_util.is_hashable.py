def is_hashable(arg):
  try:
    hash(arg)
    return True
  except TypeError:
    return False
