  @property
  def is_dynamic_size(self):
    return any(isinstance(i, Slice) and i.is_dynamic_size for i in self.indices)
