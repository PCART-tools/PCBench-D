  def __init__(self, trace: JaxprTrace, pval: PartialVal,
               recipe: JaxprTracerRecipe | None):
    assert isinstance(pval, PartialVal)
    pv, const = pval
    if isinstance(const, Tracer) and const._trace.level >= trace.level:
      raise core.escaped_tracer_error(
          const, f"Tracer from a higher level: {const} in trace {trace}")
    if isinstance(pv, DShapedArray):
      assert all(not isinstance(d, Tracer) or isinstance(d, JaxprTracer) and
                 d._trace.level == trace.level for d in pv.shape)
    self._trace = trace
    self.pval = pval
    self.recipe = recipe
