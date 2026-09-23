def _add_implicit_outputs(jaxpr: Jaxpr) -> tuple[Jaxpr, OutputType]:
  invars = [*jaxpr.constvars, *jaxpr.invars]
  expl_outvars = jaxpr.outvars

  # First do a pass to collect implicit outputs, meaning variables which occur
  # in explicit_outvars types but not in invars or to the left in outvars.
  seen: set[Var] = set(invars)
  impl_outvars = [seen.add(d) or d for x in expl_outvars if type(x) is Var and  # type: ignore
                  (seen.add(x) or type(x.aval) is DShapedArray)  # type: ignore
                  for d in x.aval.shape if type(d) is Var and d not in seen]
  outvars = [*impl_outvars, *expl_outvars]

  # Now assemble an OutputType by mapping vars in shapes to InDBIdx/OutDBIdx.
  in_map : dict[Var,  InDBIdx] = {v:  InDBIdx(i) for i, v in enumerate( invars)}
  out_map: dict[Var, OutDBIdx] = {x: OutDBIdx(i) for i, x in enumerate(outvars)
                                  if type(x) is Var}
  out_avals_ = (x.aval for x in outvars)
  out_avals = [a.update(shape=tuple(in_map.get(d, out_map.get(d))
                                    if type(d) is Var else d for d in a.shape))
               if type(a) is DShapedArray else a for a in out_avals_]
  kept_outs = [False] * len(impl_outvars) + [True] * len(expl_outvars)
  out_type = tuple(zip(out_avals, kept_outs))

  new_jaxpr = Jaxpr(jaxpr.constvars, jaxpr.invars, outvars, jaxpr.eqns,
                    jaxpr.effects, jaxpr.debug_info)
  config.enable_checks.value and core.check_jaxpr(jaxpr)
  return new_jaxpr, out_type
