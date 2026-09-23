  def new_const(self, c):
    # TODO(mattjj): for ints, or hashable consts, don't rely on id
    tracer = self.frame.constid_to_tracer.get(id(c))
    if tracer is None:
      aval = raise_to_shaped(get_aval(c), weak_type=dtypes.is_weakly_typed(c))
      aval = self._lift_tracers_in_aval(aval)
      tracer = self._new_const(aval, c)
    return tracer
