  def pure(self, val: Any) -> JaxprTracer:
    return self.new_const(val)
