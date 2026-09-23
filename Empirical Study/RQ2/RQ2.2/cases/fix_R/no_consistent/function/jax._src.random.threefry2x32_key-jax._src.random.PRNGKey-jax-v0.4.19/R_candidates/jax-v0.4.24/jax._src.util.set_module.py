def set_module(module: str) -> Callable[[T], T]:
  def wrapper(func: T) -> T:
    if module is not None:
      func.__module__ = module
    return func
  return wrapper
