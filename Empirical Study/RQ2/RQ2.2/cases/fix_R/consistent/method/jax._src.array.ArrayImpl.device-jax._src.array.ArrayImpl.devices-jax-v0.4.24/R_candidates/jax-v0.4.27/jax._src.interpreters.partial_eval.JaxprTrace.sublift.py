  def sublift(self, val: JaxprTracer) -> JaxprTracer:
    return JaxprTracer(self, val.pval, FreeVar(val))
