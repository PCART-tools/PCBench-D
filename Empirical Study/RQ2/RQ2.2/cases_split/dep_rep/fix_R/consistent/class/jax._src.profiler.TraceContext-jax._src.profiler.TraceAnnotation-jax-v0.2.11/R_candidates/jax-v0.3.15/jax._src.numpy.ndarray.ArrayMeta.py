class ArrayMeta(abc.ABCMeta):
  """Metaclass for overriding ndarray isinstance checks."""

  def __instancecheck__(self, instance):
    # Allow tracer instances with avals that are instances of UnshapedArray.
    # We could instead just declare Tracer an instance of the ndarray type, but
    # there can be traced values that are not arrays. The main downside here is
    # that isinstance(x, ndarray) might return true but
    # issubclass(type(x), ndarray) might return false for an array tracer.
    try:
      return (hasattr(instance, "aval") and
              isinstance(instance.aval, core.UnshapedArray))
    except AttributeError:
      super().__instancecheck__(instance)
