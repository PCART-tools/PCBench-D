def dce_jaxpr_closed_call_rule(used_outputs: list[bool], eqn: JaxprEqn
                               ) -> tuple[list[bool], JaxprEqn]:
  # TODO(mattjj): de-duplicate with above rule?
  jaxpr_ = eqn.params['call_jaxpr']
  closed_jaxpr, used_inputs = _cached_closed_call_dce(jaxpr_, tuple(used_outputs))
  new_params = dict(eqn.params, call_jaxpr=closed_jaxpr)
  new_eqn = new_jaxpr_eqn(
      [v for v, used in zip(eqn.invars, used_inputs) if used],
      [v for v, used in zip(eqn.outvars, used_outputs) if used],
      eqn.primitive, new_params, closed_jaxpr.effects, eqn.source_info)
  return used_inputs, new_eqn
