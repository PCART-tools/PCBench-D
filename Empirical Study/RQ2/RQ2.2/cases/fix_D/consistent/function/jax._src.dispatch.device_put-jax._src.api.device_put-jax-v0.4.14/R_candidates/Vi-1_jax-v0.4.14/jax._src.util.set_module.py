def set_module(module):
  def wrapper(func):
    if module is not None:
      func.__module__ = module
    return func
  return wrapper
