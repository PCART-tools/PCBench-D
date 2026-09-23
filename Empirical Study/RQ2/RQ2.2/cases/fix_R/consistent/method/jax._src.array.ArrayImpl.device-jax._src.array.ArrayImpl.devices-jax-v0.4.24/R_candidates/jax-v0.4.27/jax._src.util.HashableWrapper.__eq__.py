  def __eq__(self, other):
    if not isinstance(other, HashableWrapper):
      return False
    return self.x == other.x if self.hash is not None else self.x is other.x
