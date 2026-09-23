  def __getattr__(self, name):
    return getattr(self.ref, name)
