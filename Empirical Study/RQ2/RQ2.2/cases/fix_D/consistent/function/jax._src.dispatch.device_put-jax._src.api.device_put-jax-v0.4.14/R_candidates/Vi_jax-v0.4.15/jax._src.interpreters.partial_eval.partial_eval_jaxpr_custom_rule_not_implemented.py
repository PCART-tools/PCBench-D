def partial_eval_jaxpr_custom_rule_not_implemented(
    name: str, saveable: Callable[..., bool], unks_in: Sequence[bool],
    inst_in: Sequence[bool], eqn: JaxprEqn) -> PartialEvalCustomResult:
  msg = (f'custom-policy remat rule not implemented for {name}, '
         'open a feature request at https://github.com/google/jax/issues!')
  raise NotImplementedError(msg)
