class StrictABCMeta(abc.ABCMeta):
  """A variant of `abc.ABCMeta` which does not allow virtual subclasses.

  Virtual subclasses support require `abc.ABCMeta` to roundtrip through
  pure Python when doing instance/subclass checking. This if fine for ABCs
  which need virtual subclasses, but is wasteful for the ones which don't.
  """
  def register(cls, subclass):
    del subclass  # Unused.
    raise NotImplementedError(f"{cls} does not support virtual subclasses")

  __instancecheck__ = type.__instancecheck__  # type: ignore[assignment]
  __subclasscheck__ = type.__subclasscheck__  # type: ignore[assignment]
