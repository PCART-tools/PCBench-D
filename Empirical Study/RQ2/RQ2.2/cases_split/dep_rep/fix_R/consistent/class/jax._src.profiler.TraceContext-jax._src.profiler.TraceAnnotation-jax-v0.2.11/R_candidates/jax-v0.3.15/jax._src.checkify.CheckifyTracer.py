class CheckifyTracer(core.Tracer):
  def __init__(self, trace, val):
    self._trace = trace
    self.val = val
    core.get_aval(val), val
  aval = property(lambda self: core.get_aval(self.val))
  full_lower = lambda self: self
