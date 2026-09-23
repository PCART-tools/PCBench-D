class JaxprTracer(Tracer):
  __slots__ = ['pval', 'recipe']

  def __init__(self, trace: JaxprTrace, pval: PartialVal,
               recipe: JaxprTracerRecipe | None):
    assert isinstance(pval, PartialVal)
    pv, const = pval
    if isinstance(const, Tracer) and const._trace.level >= trace.level:
      raise core.escaped_tracer_error(
          const, f"Tracer from a higher level: {const} in trace {trace}")
    if isinstance(pv, DShapedArray):
      assert all(not isinstance(d, Tracer) or isinstance(d, JaxprTracer) and
                 d._trace.level == trace.level for d in pv.shape)
    self._trace = trace
    self.pval = pval
    self.recipe = recipe

  def __repr__(self):
    return f'Traced<{self.aval}:{self._trace}>'

  @property
  def aval(self) -> AbstractValue:
    return self.pval.get_aval()

  @property
  def parents(self) -> Sequence[JaxprTracer]:
    if isinstance(self.recipe, JaxprEqnRecipe):
      # TODO broadcast_in_dim can create a new tracer...
      return self.recipe.in_tracers
    elif isinstance(self.aval, DShapedArray):
      return [d for d in self.aval.shape if isinstance(d, JaxprTracer)]
    else:
      return []

  def full_lower(self):
    known = self.pval.get_known()
    if known is not None:
      return core.full_lower(known)
    else:
      return self

  def is_known(self):
    return self.pval.is_known()

  def get_referent(self):
    if self.pval.is_known():
      return get_referent(self.pval.get_known())
    elif isinstance(self.recipe, (FreeVar, ConstVar, Literal)):
      return get_referent(self.recipe.val)  # pytype: disable=attribute-error
    else:
      return self
