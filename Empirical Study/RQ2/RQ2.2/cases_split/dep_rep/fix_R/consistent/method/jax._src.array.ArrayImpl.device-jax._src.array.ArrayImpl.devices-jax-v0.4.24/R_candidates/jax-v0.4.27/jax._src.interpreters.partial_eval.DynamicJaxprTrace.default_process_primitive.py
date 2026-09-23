  def default_process_primitive(self, primitive, tracers, params):
    avals = [t.aval for t in tracers]
    out_avals, effects = primitive.abstract_eval(*avals, **params)
    # == serve as a "not xor" here.
    if not (isinstance(out_avals, (tuple,list)) == primitive.multiple_results):
      raise ValueError(f"{primitive}.abstract_eval() method should return"
                       f" a tuple or a list if {primitive}.multiple_results"
                       " is true. Otherwise it shouldn't.")
    out_avals = [out_avals] if not primitive.multiple_results else out_avals
    source_info = source_info_util.current()
    out_tracers = [DynamicJaxprTracer(self, a, source_info) for a in out_avals]
    invars = map(self.getvar, tracers)
    outvars = map(self.makevar, out_tracers)
    eqn = new_jaxpr_eqn(invars, outvars, primitive, params, effects, source_info)
    self.frame.add_eqn(eqn)
    return out_tracers if primitive.multiple_results else out_tracers.pop()
