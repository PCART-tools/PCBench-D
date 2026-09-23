  def __radd__(self, other: NameStack) -> NameStack:
    return NameStack(other.stack + self.stack)
