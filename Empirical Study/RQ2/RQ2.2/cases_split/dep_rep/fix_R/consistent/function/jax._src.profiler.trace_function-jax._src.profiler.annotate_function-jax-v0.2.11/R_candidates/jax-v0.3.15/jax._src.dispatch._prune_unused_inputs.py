def _prune_unused_inputs(
    jaxpr: core.Jaxpr) -> Tuple[core.Jaxpr, Set[int], Set[int]]:
  used = {v for v in jaxpr.outvars if isinstance(v, core.Var)}
  # TODO(zhangqiaorjc): Improve the DCE algorithm by also pruning primitive
  # applications that do not produce used outputs. Must handle side-effecting
  # primitives and nested jaxpr.
  used.update(
      v for eqn in jaxpr.eqns for v in eqn.invars if isinstance(v, core.Var))
  kept_const_idx, new_constvars = util.unzip2(
      (i, v) for i, v in enumerate(jaxpr.constvars) if v in used)
  kept_var_idx, new_invars = util.unzip2(
      (i, v) for i, v in enumerate(jaxpr.invars) if v in used)
  new_jaxpr = core.Jaxpr(new_constvars, new_invars, jaxpr.outvars, jaxpr.eqns,
                         jaxpr.effects)
  return new_jaxpr, set(kept_const_idx), set(kept_var_idx)
