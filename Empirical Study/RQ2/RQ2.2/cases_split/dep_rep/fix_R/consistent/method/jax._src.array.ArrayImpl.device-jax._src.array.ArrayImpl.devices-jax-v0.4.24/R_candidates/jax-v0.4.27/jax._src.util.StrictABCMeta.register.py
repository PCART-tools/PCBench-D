  def register(cls, subclass):
    del subclass  # Unused.
    raise NotImplementedError(f"{cls} does not support virtual subclasses")
