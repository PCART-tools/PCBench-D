  def __eq__(self, other: Any) -> bool:
    return id(self) == id(other) or self.dtype.type == other
