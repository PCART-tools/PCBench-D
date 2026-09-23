  def __eq__(self, other):
    return type(other) is KeyTy and self._impl == other._impl
