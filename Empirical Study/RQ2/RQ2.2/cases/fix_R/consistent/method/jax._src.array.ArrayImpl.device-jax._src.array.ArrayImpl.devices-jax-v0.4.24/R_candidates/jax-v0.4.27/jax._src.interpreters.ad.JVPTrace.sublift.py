  def sublift(self, val):
    return JVPTracer(self, val.primal, val.tangent)
