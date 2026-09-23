  @property
  def is_dynamic_start(self):
    return not isinstance(self.start, int)
