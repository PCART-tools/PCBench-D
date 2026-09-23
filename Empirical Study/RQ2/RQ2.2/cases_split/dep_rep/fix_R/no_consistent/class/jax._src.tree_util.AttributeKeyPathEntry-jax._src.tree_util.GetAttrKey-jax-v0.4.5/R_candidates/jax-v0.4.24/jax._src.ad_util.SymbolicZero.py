class SymbolicZero:
  def __init__(self, aval: core.AbstractValue) -> None:
    self.aval = aval

  def __repr__(self) -> str:
    return self.__class__.__name__

  # TODO(mattjj,frostig): this forwards attr lookup to self.aval delegate;
  # should dedup with core.Tracer.__getattr__ which does the same thing
  def __getattr__(self, name):
    # if the aval property raises an AttributeError, gets caught here
    try:
      attr = getattr(self.aval, name)
    except KeyError as err:
      raise AttributeError(
          f"{self.__class__.__name__} has no attribute {name}"
      ) from err
    else:
      t = type(attr)
      if t is core.aval_property:
        return attr.fget(self)
      elif t is core.aval_method:
        return types.MethodType(attr.fun, self)
      else:
        return attr
