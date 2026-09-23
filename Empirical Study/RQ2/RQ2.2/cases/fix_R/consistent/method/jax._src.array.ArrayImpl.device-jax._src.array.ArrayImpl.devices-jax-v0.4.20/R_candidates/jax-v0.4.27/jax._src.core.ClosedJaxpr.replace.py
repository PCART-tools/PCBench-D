  def replace(self, *, jaxpr=None, consts=None):
    jaxpr = self.jaxpr if jaxpr is None else jaxpr
    consts = self.consts if consts is None else consts
    return ClosedJaxpr(jaxpr, consts)
