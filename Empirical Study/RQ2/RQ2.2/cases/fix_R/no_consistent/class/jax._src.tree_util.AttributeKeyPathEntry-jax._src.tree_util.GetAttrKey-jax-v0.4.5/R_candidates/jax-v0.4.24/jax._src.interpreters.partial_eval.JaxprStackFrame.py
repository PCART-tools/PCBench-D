class JaxprStackFrame:
  gensym: Callable[[AbstractValue], Var]
  tracer_to_var: dict[TracerId, Var]
  constid_to_tracer: dict[ConstId, Tracer]
  constvar_to_val: dict[Var, Any]
  tracers: list[DynamicJaxprTracer]  # hold onto strong refs for all tracers
  eqns: list[JaxprEqn]
  invars: list[Var]
  effects: core.Effects
  attrs_tracked: list[tuple[Any, str]]
  attrs_inits: list
  attrs_vars: list[Var]
  debug_info: DebugInfo | None

  def __init__(self):
    self.gensym = core.gensym()
    self.tracer_to_var = {}
    self.constid_to_tracer = {}
    self.constvar_to_val = {}
    self.tracers = []   # circ refs, frame->tracer->trace->main->frame,
    self.eqns = []      # cleared when we pop frame from main
    self.invars = []
    self.effects = set()
    self.attrs_tracked = []
    self.attrs_inits = []
    self.attrs_vars = []
    self.debug_info = None

  def add_eqn(self, eqn: core.JaxprEqn):
    self.eqns.append(eqn)

  def to_jaxpr(self, out_tracers: Sequence[Tracer]
               ) -> tuple[Jaxpr, list[Any], list[tuple[Any, str]]]:
    # It's not necessary, but we keep the tracer-to-var mapping injective:
    assert len(self.tracer_to_var) == len(set(self.tracer_to_var.values()))
    invars = self.attrs_vars + self.invars
    state_outvars    = [self.tracer_to_var[id(t)] for t in get_states(self.attrs_tracked)]
    explicit_outvars = [self.tracer_to_var[id(t)] for t in out_tracers]
    outvars = state_outvars + explicit_outvars
    constvars, constvals = unzip2(self.constvar_to_val.items())
    jaxpr_effects = make_jaxpr_effects(constvars, self.invars, explicit_outvars, self.eqns)
    jaxpr = Jaxpr(constvars, invars, outvars, self.eqns, jaxpr_effects)
    jaxpr, constvals = _const_folding_and_forwarding(jaxpr, constvals)
    jaxpr, constvals = _inline_literals(jaxpr, constvals)  # type: ignore
    set_states(self.attrs_tracked, self.attrs_inits)
    return jaxpr, list(constvals), self.attrs_tracked

  def to_jaxpr2(self, out_tracers):
    # It's not necessary, but we keep the tracer-to-var mapping injective:
    assert len(self.tracer_to_var) == len(set(self.tracer_to_var.values()))
    constvars, constvals = unzip2(self.constvar_to_val.items())
    expl_outvars = [self.tracer_to_var[id(t)] for t in out_tracers]
    jaxpr_effects = make_jaxpr_effects(constvars, self.invars, expl_outvars,
                                        self.eqns)
    jaxpr = Jaxpr(constvars, self.invars, expl_outvars, self.eqns,
                  jaxpr_effects)
    # We can't run check_jaxpr until after we normalize.
    jaxpr, constvals = _const_folding_and_forwarding(jaxpr, constvals)
    jaxpr, constvals = _inline_literals(jaxpr, constvals)
    jaxpr, out_type = _add_implicit_outputs(jaxpr)
    config.enable_checks.value and core.check_jaxpr(jaxpr)
    return jaxpr, out_type, constvals

  def newvar(self, aval):
    if isinstance(aval, DShapedArray):
      # this aval may have tracers in it, so we replace those with variables
      new_shape = [self.tracer_to_var[id(d)] if isinstance(d, Tracer) else d
                   for d in aval.shape]
      aval = aval.update(shape=tuple(new_shape))
    return self.gensym(aval)

  def find_progenitors(self, tracer):
    var = self.tracer_to_var.get(id(tracer))
    if not var:
      return None, None
    active_vars = {var}
    for eqn in self.eqns[::-1]:
      produced = set(eqn.outvars) & active_vars
      if produced:
        active_vars.difference_update(produced)
        active_vars.update(eqn.invars)
    invar_positions = [i for i, v in enumerate(self.invars) if v in active_vars]
    constvars = active_vars & set(self.constvar_to_val)
    const_eqns = [eqn for eqn in self.eqns if set(eqn.invars) & constvars]
    return invar_positions, const_eqns
