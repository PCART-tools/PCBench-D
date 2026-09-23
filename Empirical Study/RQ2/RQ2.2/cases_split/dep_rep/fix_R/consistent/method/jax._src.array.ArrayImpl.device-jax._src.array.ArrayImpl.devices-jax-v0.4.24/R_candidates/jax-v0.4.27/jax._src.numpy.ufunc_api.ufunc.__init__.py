  def __init__(self, func: Callable[..., Any], /,
               nin: int, nout: int, *,
               name: str | None = None,
               nargs: int | None = None,
               identity: Any = None, update_doc=False):
    # We want ufunc instances to work properly when marked as static,
    # and for this reason it's important that their properties not be
    # mutated. We prevent this by storing them in a dunder attribute,
    # and accessing them via read-only properties.
    if update_doc:
      self.__doc__ = func.__doc__
    self.__name__ = name or func.__name__
    self.__static_props = {
      'func': func,
      'call': vectorize(func),
      'nin': operator.index(nin),
      'nout': operator.index(nout),
      'nargs': operator.index(nargs or nin),
      'identity': identity
    }
