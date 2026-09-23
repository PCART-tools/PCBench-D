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
