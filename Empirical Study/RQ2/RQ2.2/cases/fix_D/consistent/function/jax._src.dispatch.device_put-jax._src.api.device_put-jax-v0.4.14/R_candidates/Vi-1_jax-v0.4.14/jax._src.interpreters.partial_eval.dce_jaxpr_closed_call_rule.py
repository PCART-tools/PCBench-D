def dce_jaxpr_closed_call_rule(used_outputs: list[bool], eqn: JaxprEqn
                               ) -> tuple[list[bool], JaxprEqn]:
  # TODO(mattjj): de-duplicate with above rule?
  jaxpr_ = eqn.params['call_jaxpr']
  jaxpr, consts = jaxpr_.jaxpr, jaxpr_.consts
  new_jaxpr, used_inputs = dce_jaxpr(jaxpr, used_outputs)
  new_params = dict(eqn.params, call_jaxpr=core.ClosedJaxpr(new_jaxpr, consts))
  new_eqn = new_jaxpr_eqn(
      [v for v, used in zip(eqn.invars, used_inputs) if used],
      [v for v, used in zip(eqn.outvars, used_outputs) if used],
      eqn.primitive, new_params, new_jaxpr.effects, eqn.source_info)
  return used_inputs, new_eqn
