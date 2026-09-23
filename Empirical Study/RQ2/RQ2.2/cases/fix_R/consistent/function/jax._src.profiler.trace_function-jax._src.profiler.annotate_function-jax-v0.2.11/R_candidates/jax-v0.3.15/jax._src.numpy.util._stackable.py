def _stackable(*args):
  return all(type(arg) in stackables for arg in args)
