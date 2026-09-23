  @property
  def in_avals(self):
    return [v.aval for v in self.jaxpr.invars]
