def custom_jvp_jaxpr_custom_partial_eval_rule(
    saveable: Callable[..., bool], unks_in: List[bool], inst_in: List[bool],
    eqn: core.JaxprEqn
  ) -> Tuple[Optional[core.JaxprEqn], core.JaxprEqn, List[bool], List[bool], List[core.Var]]:
  # It doesn't make sense to unzip (i.e. break up) a custom_jvp function into
  # constituent parts, so we always perform full remat. An alternative would be
  # to allow the policy function to decide whether the value of a
  # custom_jvp-decorated function's application should be saved or not.
  # TODO(mattjj,jekbradbury): the user writing the custom_jvp-decorated function
  # probably has a better idea for what to do under remat (e.g. if the function
  # contains dots or not), so we should allow for more expressive interaction
  # (e.g. allow the policy to depend on which custom_jvp-decorated function is
  # being applied, or annotating the behavior where custom_vjp is called.)
  inst_out = [True] * len(eqn.outvars)
  new_inst = [x for x, inst in zip(eqn.invars, inst_in)
              if type(x) is core.Var and not inst]
  if any(unks_in):
    unks_out = [True] * len(eqn.outvars)
    return None, eqn, unks_out, inst_out, new_inst
  else:
    unks_out = [False] * len(eqn.outvars)
    return eqn, eqn, unks_out, inst_out, new_inst
