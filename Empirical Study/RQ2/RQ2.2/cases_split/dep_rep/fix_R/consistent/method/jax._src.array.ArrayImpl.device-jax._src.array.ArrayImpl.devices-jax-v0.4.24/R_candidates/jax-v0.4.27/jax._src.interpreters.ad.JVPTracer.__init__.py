  def __init__(self, trace, primal, tangent):
    if config.enable_checks.value:
      _primal_tangent_shapes_match(primal, tangent)
    self._trace = trace
    self.primal = primal
    self.tangent = tangent
