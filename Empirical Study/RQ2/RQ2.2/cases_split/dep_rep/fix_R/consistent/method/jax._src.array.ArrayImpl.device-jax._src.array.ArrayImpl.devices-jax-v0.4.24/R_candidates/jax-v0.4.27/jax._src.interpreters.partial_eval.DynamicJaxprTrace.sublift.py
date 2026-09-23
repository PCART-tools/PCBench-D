  def sublift(self, t):
    # When lifting closed-over tracers corresponding to this same trace, the
    # variable to lift could have tracers (representing axis size variables) in
    # its shape. We must lift those too!
    tracer = self.frame.constid_to_tracer.get(id(t))
    if tracer is None:
      aval = raise_to_shaped(get_aval(t), weak_type=dtypes.is_weakly_typed(t))
      aval = self._lift_tracers_in_aval(aval)
      tracer = self._new_const(aval, t)
    return tracer
