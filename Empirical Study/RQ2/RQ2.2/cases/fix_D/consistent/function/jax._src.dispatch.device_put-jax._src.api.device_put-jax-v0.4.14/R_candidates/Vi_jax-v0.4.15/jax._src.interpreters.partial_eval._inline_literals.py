def _inline_literals(
    jaxpr: Jaxpr, constvals: Sequence[Any]
) -> tuple[Jaxpr, list[Any]]:
  # This function also prunes unused constants and inserts `dropvar` symbols.
  input_effects = {eff for eff in jaxpr.effects
                   if isinstance(eff, effects.JaxprInputEffect)}
  # Don't inline any literal with an input effect
  has_input_effect = [any(eff.input_index == i for eff in input_effects)
                      for i in range(len(constvals))]
  lits = {v: Literal(c, v.aval) for v, c, e in zip(jaxpr.constvars, constvals,
                                                   has_input_effect)
          if type(c) in core.literalable_types and not np.shape(c) and not e}
  lit: Callable[[Var], Literal | None] = lits.get
  newname: Callable[[AbstractValue], Var] = core.gensym()
  newvars: dict[Var, Var] = {}
  newvar = lambda aval: newname(_substitute_vars_in_type(lits, newvars, aval))
  var = lambda v: newvars.get(v) or newvars.setdefault(v, newvar(v.aval))
  dropvar = lambda aval: DropVar(_substitute_vars_in_type(lits, newvars, aval))

  def vars_in_shape(aval: AbstractValue) -> Sequence[Var]:
    if isinstance(aval, DShapedArray):
      return [d for d in aval.shape if isinstance(d, Var)]
    return []

  used = {v for eqn in jaxpr.eqns for invar in eqn.invars
          for v in it.chain([invar], vars_in_shape(invar.aval))}
  used |= {v for outvar in jaxpr.outvars
           for v in it.chain([outvar], vars_in_shape(outvar.aval))}
  new_constvars = [var(v) for v in jaxpr.constvars if v in used and not lit(v)]
  new_constvals = [c for v, c in zip(jaxpr.constvars, constvals)
                   if v in used and not lit(v)]
  new_invars = [var(v) for v in jaxpr.invars]
  new_eqns = []
  for eqn in jaxpr.eqns:
    invars = [lit(v) or var(v) for v in eqn.invars]
    outvars = [var(v) if v in used else dropvar(v.aval) for v in eqn.outvars]
    new_eqns.append(eqn.replace(invars=invars, outvars=outvars))
  new_outvars = [lit(v) or var(v) for v in jaxpr.outvars]
  jaxpr_effects = make_jaxpr_effects(new_constvars, new_invars, new_outvars,
                                      new_eqns)
  new_jaxpr = Jaxpr(new_constvars, new_invars, new_outvars, new_eqns,
                    jaxpr_effects, jaxpr.debug_info)
  return new_jaxpr, new_constvals
