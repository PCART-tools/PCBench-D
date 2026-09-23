  def new_instantiated_const(self, val) -> JaxprTracer:
    aval = get_aval(val)
    if isinstance(aval, DShapedArray):
      shape = [self.new_instantiated_const(d)
               if isinstance(d, Tracer) and d._trace.level < self.level else d
               for d in aval.shape]
      aval = aval.update(shape=tuple(shape))
    return JaxprTracer(self, PartialVal.unknown(aval), ConstVar(val))
