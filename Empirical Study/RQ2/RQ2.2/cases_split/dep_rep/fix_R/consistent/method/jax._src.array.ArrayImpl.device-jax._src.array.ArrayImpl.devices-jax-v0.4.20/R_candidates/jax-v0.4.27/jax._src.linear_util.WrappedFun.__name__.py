  @property
  def __name__(self):
    return getattr(self.f, '__name__', '<unnamed wrapped function>')
