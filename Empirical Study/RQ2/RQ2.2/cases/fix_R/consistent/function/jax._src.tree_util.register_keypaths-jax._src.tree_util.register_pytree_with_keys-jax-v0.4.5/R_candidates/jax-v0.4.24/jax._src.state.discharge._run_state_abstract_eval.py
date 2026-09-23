def _run_state_abstract_eval(*avals: core.AbstractValue, jaxpr: core.Jaxpr,
                             which_linear: tuple[bool, ...]):
  del which_linear
  # When we abstractly evaluate `run_state`, we want to keep track of which
  # input avals are `Ref`s and which are not. If an aval is a `Ref`, we want to
  # "propagate" out its inner effects. Otherwise, the effects are local to this
  # `run_state`.
  is_ref = {i for i, aval in enumerate(avals) if isinstance(aval, AbstractRef)}
  nonlocal_effects = {e for e in jaxpr.effects
                      if (isinstance(e, RefEffect) and e.input_index in is_ref)
                      or not isinstance(e, RefEffect)}
  return avals, nonlocal_effects
