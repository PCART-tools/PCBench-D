  def lift(self, val: Tracer) -> JaxprTracer:
    return self.new_const(val)
