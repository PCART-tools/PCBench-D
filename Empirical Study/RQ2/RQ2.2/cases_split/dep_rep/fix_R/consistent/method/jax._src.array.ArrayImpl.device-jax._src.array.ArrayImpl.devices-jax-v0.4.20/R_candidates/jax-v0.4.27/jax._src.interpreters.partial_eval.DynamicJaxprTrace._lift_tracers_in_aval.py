  def _lift_tracers_in_aval(self, aval):
    if (not isinstance(aval, DShapedArray) or
        not any(isinstance(d, Tracer) for d in aval.shape)):
      return aval
    shape = [self.full_raise(d) if isinstance(d, Tracer) else d
             for d in aval.shape]
    return aval.update(shape=tuple(shape))
