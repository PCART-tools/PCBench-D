  def __eq__(self, other):
    return (type(self) is type(other) and self.inner_aval == other.inner_aval
            and self.memory_space == other.memory_space)
