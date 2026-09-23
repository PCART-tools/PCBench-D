def discharge_state(jaxpr: core.Jaxpr, consts: Sequence[Any], * ,
                    should_discharge: bool | Sequence[bool] = True
                    ) -> tuple[core.Jaxpr, list[Any]]:
  """Converts a jaxpr that takes in `Ref`s into one that doesn't."""
  if isinstance(should_discharge, bool):
    should_discharge = [should_discharge] * len(jaxpr.invars)
  in_avals = [v.aval.inner_aval
              if isinstance(v.aval, AbstractRef) and d
              else v.aval for v, d in zip(jaxpr.invars, should_discharge)]
  eval_jaxpr = lu.wrap_init(partial(_eval_jaxpr_discharge_state, jaxpr,
                                    should_discharge, consts))
  new_jaxpr, _ , new_consts, () = pe.trace_to_jaxpr_dynamic(eval_jaxpr, in_avals)
  return new_jaxpr, new_consts
