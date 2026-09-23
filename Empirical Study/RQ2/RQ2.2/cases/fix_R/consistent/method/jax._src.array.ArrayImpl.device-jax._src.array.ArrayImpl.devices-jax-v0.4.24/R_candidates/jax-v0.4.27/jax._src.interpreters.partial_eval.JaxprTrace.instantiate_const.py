  def instantiate_const(self, tracer: JaxprTracer) -> JaxprTracer:
    const = tracer.pval.get_known()
    if const is None:
      return tracer
    else:
      if type(const) in core.literalable_types and np.shape(const) == ():
        return self.new_instantiated_literal(const)
      else:
        return self.new_instantiated_const(const)
