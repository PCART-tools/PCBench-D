class ClosedJaxpr:
  __slots__ = ['__weakref__', '_jaxpr', '_consts']

  _jaxpr: Jaxpr
  _consts: list[Any]

  jaxpr = property(lambda self: self._jaxpr)
  consts = property(lambda self: self._consts)

  def __init__(self, jaxpr: Jaxpr, consts: Sequence):
    assert len(consts) == len(jaxpr.constvars)
    # assert not any(isinstance(c, Tracer) for c in consts)  # TODO(mattjj): enable
    self._jaxpr = jaxpr
    self._consts = list(consts)

  @property
  def in_avals(self):
    return [v.aval for v in self.jaxpr.invars]

  @property
  def out_avals(self):
    return [v.aval for v in self.jaxpr.outvars]

  @property
  def literals(self):
    return self.consts  # backwards compatible alias

  @property
  def eqns(self):
    return self.jaxpr.eqns

  @property
  def effects(self) -> Effects:
    return self.jaxpr.effects

  def map_jaxpr(self, f):
    return ClosedJaxpr(f(self.jaxpr), self.consts)

  def replace(self, *, jaxpr=None, consts=None):
    jaxpr = self.jaxpr if jaxpr is None else jaxpr
    consts = self.consts if consts is None else consts
    return ClosedJaxpr(jaxpr, consts)

  def __str__(self): return str(self.jaxpr)
  def __repr__(self): return repr(self.jaxpr)

  def pretty_print(self, *, source_info=False, print_shapes=True,
                   name_stack=False, custom_pp_eqn_rules=True,
                   print_effects=False, **kwargs):
    return self.jaxpr.pretty_print(
        source_info=source_info,
        print_shapes=print_shapes,
        name_stack=name_stack,
        custom_pp_eqn_rules=custom_pp_eqn_rules,
        print_effects=print_effects,
        **kwargs)

  def _repr_pretty_(self, p, cycle):
    return p.text(self.pretty_print(use_color=True))
