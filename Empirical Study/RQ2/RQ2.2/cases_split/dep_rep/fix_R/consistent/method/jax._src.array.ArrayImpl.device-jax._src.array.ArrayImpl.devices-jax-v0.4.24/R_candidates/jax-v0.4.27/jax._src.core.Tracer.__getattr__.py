  def __getattr__(self, name):
    # if the aval property raises an AttributeError, gets caught here
    assert not config.enable_checks.value or name != "aval"

    try:
      attr = getattr(self.aval, name)
    except AttributeError as err:
      raise AttributeError(
          f"{self.__class__.__name__} has no attribute {name}"
      ) from err
    else:
      t = type(attr)
      if t is aval_property:
        return attr.fget(self)
      elif t is aval_method:
        return types.MethodType(attr.fun, self)
      else:
        return attr
