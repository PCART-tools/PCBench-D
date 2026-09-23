  def update(self, inner_aval=None):
    if inner_aval is None:
      return AbstractRef(self.inner_aval)
    return AbstractRef(inner_aval)
