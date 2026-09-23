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
