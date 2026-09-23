  def __hash__(self):
    return self.hash if self.hash is not None else id(self.x)
