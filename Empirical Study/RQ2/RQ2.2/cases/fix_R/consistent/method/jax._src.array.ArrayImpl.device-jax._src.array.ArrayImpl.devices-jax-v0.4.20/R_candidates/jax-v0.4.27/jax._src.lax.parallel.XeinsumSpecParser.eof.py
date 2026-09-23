  @property
  def eof(self):
    return self.pos == len(self.spec)
