def _eqn_replicas(eqn: core.JaxprEqn) -> int:
  call_jaxpr = eqn.params.get("call_jaxpr")
  if call_jaxpr:
    return eqn.params.get('axis_size', 1) * jaxpr_replicas(call_jaxpr)
  elif eqn.primitive in xla.initial_style_primitives:
    return _initial_style_primitive_replicas(eqn.params)
  else:
    return 1
