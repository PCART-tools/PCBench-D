  def __eq__(self, other):
    return isinstance(other, TracerAsName) and self.ref is other.ref
