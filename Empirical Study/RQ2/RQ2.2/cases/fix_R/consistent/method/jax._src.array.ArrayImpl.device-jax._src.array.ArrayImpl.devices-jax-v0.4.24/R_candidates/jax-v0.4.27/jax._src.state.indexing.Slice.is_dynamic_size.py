  @property
  def is_dynamic_size(self):
    return not isinstance(self.size, int)
