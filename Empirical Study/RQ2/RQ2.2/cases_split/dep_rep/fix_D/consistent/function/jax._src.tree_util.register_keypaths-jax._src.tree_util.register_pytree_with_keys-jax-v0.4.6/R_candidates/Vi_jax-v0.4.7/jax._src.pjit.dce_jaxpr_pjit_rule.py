def dce_jaxpr_pjit_rule(used_outputs: List[bool], eqn: core.JaxprEqn
                        ) -> Tuple[List[bool], Optional[core.JaxprEqn]]:
  dced_jaxpr, used_inputs = _dce_jaxpr_pjit(
      eqn.params['jaxpr'], tuple(used_outputs))

  def keep_where(xs, keeps):
    return tuple(x for x, keep in zip(xs, keeps) if keep)

  eqn_params = eqn.params
  new_params = dict(
      eqn_params,
      jaxpr=dced_jaxpr,
      in_shardings=keep_where(eqn_params["in_shardings"], used_inputs),
      out_shardings=keep_where(eqn_params["out_shardings"], used_outputs),
      donated_invars=keep_where(eqn_params["donated_invars"], used_inputs),
  )
  if not any(used_inputs) and not any(used_outputs) and not dced_jaxpr.effects:
    return used_inputs, None
  else:
    new_eqn = core.new_jaxpr_eqn(
        [v for v, used in zip(eqn.invars, used_inputs) if used],
        [v for v, used in zip(eqn.outvars, used_outputs) if used],
        eqn.primitive, new_params, dced_jaxpr.effects, eqn.source_info)
    return used_inputs, new_eqn
