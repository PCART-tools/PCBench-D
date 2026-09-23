@for_p.def_effectful_abstract_eval
def _for_abstract_eval(*avals, jaxpr, **__):
  # Find out for each of the `Ref`s in our jaxpr what effects they have.
  jaxpr_aval_effects = state_types.get_ref_state_effects(
      [v.aval for v in jaxpr.invars], jaxpr.effects)[1:]
  aval_effects = [{eff.replace(input_index=eff.input_index - 1)
                      for eff in effs} for aval, effs
                  in zip(avals, jaxpr_aval_effects)
                  if isinstance(aval, AbstractRef)]
  nonlocal_state_effects = core.join_effects(*aval_effects)
  return list(avals), nonlocal_state_effects
