  def __add__(self, other: NameStack) -> NameStack:
    return NameStack(self.stack + other.stack)
