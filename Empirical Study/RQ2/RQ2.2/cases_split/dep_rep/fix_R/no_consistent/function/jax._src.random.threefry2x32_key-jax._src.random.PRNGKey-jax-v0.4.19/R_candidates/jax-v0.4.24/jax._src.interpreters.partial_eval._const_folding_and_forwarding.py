def _const_folding_and_forwarding(
    jaxpr: Jaxpr, constvals: Sequence[Any]) -> tuple[Jaxpr, tuple[Any, ...]]:
  consts: dict[Var, Any] = dict(zip(jaxpr.constvars, constvals))
  var_subs: dict[Var, Var] = {}  # not Dict[Var, Atom] b/c literals not inlined
  new_eqns = []
  def apply_var_sub(a: Atom) -> Atom:
    return var_subs.get(a, a) if isinstance(a, Var) else a
  for eqn in jaxpr.eqns:
    # always apply invar substitutions
    eqn = eqn.replace(invars=[apply_var_sub(v) for v in eqn.invars])
    # if any inputs are constants and we have a constant-folding rule, apply it
    has_input_effect = any(isinstance(eff, effects.JaxprInputEffect)
                           for eff in eqn.effects)
    if (eqn.primitive in const_fold_rules and any(v in consts for v in eqn.invars)
        and not has_input_effect):
      consts_in = [consts.get(v) if isinstance(v, Var) else None
                   for v in eqn.invars]
      consts_out, new_eqn = const_fold_rules[eqn.primitive](consts_in, eqn)
      assert (new_eqn is None) == all(c is not None for c in consts_out)
      for v, c in zip(eqn.outvars, consts_out):
        if c is not None: consts[v] = c
      if new_eqn is None: continue
      else: eqn = new_eqn
    # if the application trivially maps some inputs to outputs, simplify
    if eqn.primitive in forwarding_rules and not has_input_effect:
      fwd_vars, new_eqn = forwarding_rules[eqn.primitive](eqn)
      assert (new_eqn is None) == all(v is not None for v in fwd_vars)
      for v_orig, v_new in zip(eqn.outvars, fwd_vars):
        if v_new is not None: var_subs[v_orig] = v_new
      if new_eqn is None: continue
      else: eqn = new_eqn
    new_eqns.append(eqn)
  new_constvars, new_constvals = unzip2(consts.items())
  new_outvars = [apply_var_sub(v) for v in jaxpr.outvars]
  jaxpr_effects = make_jaxpr_effects(new_constvars, jaxpr.invars, new_outvars,
                                      new_eqns)
  new_jaxpr = Jaxpr(new_constvars, jaxpr.invars, new_outvars, new_eqns,
                    jaxpr_effects, jaxpr.debug_info)
  return new_jaxpr, new_constvals
