  def __eq__(self, other):
    return type(other) is _TempAxisName and self.id == other.id
