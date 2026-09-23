  def __lt__(self, other):
    return type(other) is _TempAxisName and self.id < other.id
