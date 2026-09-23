  def __init__(self, jaxpr: core.ClosedJaxpr, out_tree):
    self.jaxpr = jaxpr
    self.out_tree = out_tree
