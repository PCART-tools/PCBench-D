  def __new__(klass, func, *args, **kw):
    # In Python 3.10+, if func is itself a functools.partial instance,
    # functools.partial.__new__ would merge the arguments of this Partial
    # instance with the arguments of the func. We box func in a class that does
    # not (yet) have a `func` attribute to defeat this optimization, since we
    # care exactly which arguments are considered part of the pytree.
    if isinstance(func, functools.partial):
      original_func = func
      func = _HashableCallableShim(original_func)
      out = super().__new__(klass, func, *args, **kw)
      func.func = original_func.func
      func.args = original_func.args
      func.keywords = original_func.keywords
      return out
    else:
      return super().__new__(klass, func, *args, **kw)
