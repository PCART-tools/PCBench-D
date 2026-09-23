class JVPTracer(Tracer):
  __slots__ = ['primal', 'tangent']

  def __init__(self, trace, primal, tangent):
    if config.enable_checks.value:
      _primal_tangent_shapes_match(primal, tangent)
    self._trace = trace
    self.primal = primal
    self.tangent = tangent

  @property
  def aval(self):
    # TODO(dougalm): add epsilon ball
    return get_aval(self.primal)

  def full_lower(self):
    if type(self.tangent) is Zero:
      return core.full_lower(self.primal)
    else:
      return self
