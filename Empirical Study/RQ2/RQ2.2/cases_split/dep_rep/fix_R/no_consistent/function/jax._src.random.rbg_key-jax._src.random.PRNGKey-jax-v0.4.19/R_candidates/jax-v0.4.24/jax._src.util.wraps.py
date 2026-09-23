def wraps(
    wrapped: Callable,
    namestr: str | None = None,
    docstr: str | None = None,
    **kwargs,
) -> Callable[[T], T]:
  """
  Like functools.wraps, but with finer-grained control over the name and docstring
  of the resulting function.
  """
  def wrapper(fun: T) -> T:
    try:
      name = getattr(wrapped, "__name__", "<unnamed function>")
      doc = getattr(wrapped, "__doc__", "") or ""
      fun.__dict__.update(getattr(wrapped, "__dict__", {}))
      fun.__annotations__ = getattr(wrapped, "__annotations__", {})
      fun.__name__ = name if namestr is None else namestr.format(fun=name)
      fun.__module__ = getattr(wrapped, "__module__", "<unknown module>")
      fun.__doc__ = (doc if docstr is None
                     else docstr.format(fun=name, doc=doc, **kwargs))
      fun.__qualname__ = getattr(wrapped, "__qualname__", fun.__name__)
      fun.__wrapped__ = wrapped
    finally:
      return fun
  return wrapper
