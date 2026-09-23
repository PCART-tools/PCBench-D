  def new_const(self, val) -> JaxprTracer:
    if isinstance(val, Tracer) and val._trace.level == self.level:
      raise Exception
    return JaxprTracer(self, PartialVal.known(val), None)
