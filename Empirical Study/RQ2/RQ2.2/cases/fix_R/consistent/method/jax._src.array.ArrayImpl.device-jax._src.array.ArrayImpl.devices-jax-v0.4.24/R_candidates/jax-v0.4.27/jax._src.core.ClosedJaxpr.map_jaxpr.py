  def map_jaxpr(self, f):
    return ClosedJaxpr(f(self.jaxpr), self.consts)
