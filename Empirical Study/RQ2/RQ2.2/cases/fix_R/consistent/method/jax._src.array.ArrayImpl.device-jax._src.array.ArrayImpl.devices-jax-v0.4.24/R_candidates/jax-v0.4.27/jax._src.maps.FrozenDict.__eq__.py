  def __eq__(self, other):
    return isinstance(other, FrozenDict) and self.contents == other.contents
