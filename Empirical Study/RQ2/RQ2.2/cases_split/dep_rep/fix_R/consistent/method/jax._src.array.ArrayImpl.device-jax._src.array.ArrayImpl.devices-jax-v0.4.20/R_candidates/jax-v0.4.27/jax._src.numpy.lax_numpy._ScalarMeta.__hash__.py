  def __hash__(self) -> int:
    return hash(self.dtype.type)
