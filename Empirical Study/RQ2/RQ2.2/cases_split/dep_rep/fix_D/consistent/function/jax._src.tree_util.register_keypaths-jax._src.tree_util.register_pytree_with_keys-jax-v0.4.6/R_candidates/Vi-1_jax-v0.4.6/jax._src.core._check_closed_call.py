def _check_closed_call(*in_atoms, call_jaxpr):
  in_avals = [x.aval for x in in_atoms]
  if list(in_avals) != list(call_jaxpr.in_avals):
    raise JaxprTypeError("Closed call in_avals mismatch")
  return call_jaxpr.out_avals, call_jaxpr.effects
