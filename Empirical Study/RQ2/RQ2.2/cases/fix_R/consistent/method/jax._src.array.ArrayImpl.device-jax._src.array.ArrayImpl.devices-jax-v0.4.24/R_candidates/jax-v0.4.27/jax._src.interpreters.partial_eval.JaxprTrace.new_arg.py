  def new_arg(self, pval: PartialVal) -> JaxprTracer:
    const = pval.get_known()
    # XXX: Think twice before changing this constant argument pruning!
    # This has really important consequences for partial_eval_jaxpr.
    # Most importantly, this guarantees that the unknown jaxpr never uses
    # known inputs (if it needs them, then they get passed through residuals).
    if const is None:
      aval = pval.get_aval()
      if type(aval) is DShapedArray:
        shape = [self.new_instantiated_const(d)
                 if isinstance(d, Tracer) and d._trace.level < self.level else d
                 for d in aval.shape]
        aval = aval.update(shape=tuple(shape))
      return JaxprTracer(self, PartialVal.unknown(aval), LambdaBinding())
    else:
      return self.new_const(const)
