def fun_sourceinfo(fun: Callable) -> str | None:
  while isinstance(fun, partial):
    fun = fun.func
  fun = inspect.unwrap(fun)
  try:
    filename = fun.__code__.co_filename
    lineno = fun.__code__.co_firstlineno
    return f"{fun.__name__} at {filename}:{lineno}"
  except AttributeError:
    return None
