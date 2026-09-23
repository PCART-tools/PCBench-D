  @property
  def out_avals(self):
    return [v.aval for v in self.jaxpr.outvars]
