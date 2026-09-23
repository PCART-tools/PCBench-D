  def replace(self, *, input_index: Any | None = None):
    if input_index is None:
      input_index = self.input_index
    return self.__class__(input_index)
