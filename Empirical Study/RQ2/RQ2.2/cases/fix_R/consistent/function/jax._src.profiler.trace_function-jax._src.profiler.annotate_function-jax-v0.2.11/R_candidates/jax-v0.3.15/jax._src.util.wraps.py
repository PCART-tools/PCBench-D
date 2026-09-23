@curry
def wraps(wrapped, fun, namestr="{fun}", docstr="{doc}", **kwargs):
  """
  Like functools.wraps, but with finer-grained control over the name and docstring
  of the resulting function.
  """
  try:
    name = getattr(wrapped, "__name__", "<unnamed function>")
    doc = getattr(wrapped, "__doc__", "") or ""
    fun.__dict__.update(getattr(wrapped, "__dict__", {}))
    fun.__annotations__ = getattr(wrapped, "__annotations__", {})
    fun.__name__ = namestr.format(fun=name)
    fun.__module__ = getattr(wrapped, "__module__", "<unknown module>")
    fun.__doc__ = docstr.format(fun=name, doc=doc, **kwargs)
    fun.__qualname__ = getattr(wrapped, "__qualname__", fun.__name__)
    fun.__wrapped__ = wrapped
  finally:
    return fun
