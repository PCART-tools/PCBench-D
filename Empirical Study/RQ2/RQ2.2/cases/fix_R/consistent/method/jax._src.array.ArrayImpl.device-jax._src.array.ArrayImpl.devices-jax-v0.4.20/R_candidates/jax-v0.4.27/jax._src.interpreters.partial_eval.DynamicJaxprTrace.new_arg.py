  def new_arg(self, aval):
    tracer = DynamicJaxprTracer(self, aval, source_info_util.current())
    self.frame.tracers.append(tracer)
    self.frame.tracer_to_var[id(tracer)] = var = self.frame.newvar(aval)
    self.frame.invars.append(var)
    return tracer
