  def __eq__(self, other):
    if not isinstance(other, JaxprInputEffect):
      return NotImplemented
    return self.input_index == other.input_index
