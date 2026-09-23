def _check_call(ctx_factory, prim, in_atoms, params):
  if "call_jaxpr" not in params:
    raise JaxprTypeError(
        f"Call primitive {prim} missing 'call_jaxpr' parameter")
  call_jaxpr = params["call_jaxpr"]

  if len(in_atoms) != len(call_jaxpr.invars):
    raise JaxprTypeError(f"Call primitive {prim} with {len(in_atoms)} "
                         f"operands cannot call jaxpr with "
                         f"{len(call_jaxpr.invars)} inputs")

  # Check `call_jaxpr` can be applied to in_atoms.
  env: Dict[Var, Atom] = {}
  def substitute(aval: AbstractValue):
    if isinstance(aval, DShapedArray):
      aval = aval.update(shape=tuple([env.get(d, d) for d in aval.shape]))  # type: ignore
    return aval
  for v, x in zip(call_jaxpr.invars, in_atoms):
    if not typecompat(substitute(v.aval), x.aval):
      # TODO(mattjj): vars in error message are confusing b/c of Var.__repr__
      raise JaxprTypeError(f"Call primitive {prim} passes operand {x} of type "
                           f"{x.aval} to jaxpr expecting type "
                           f"{substitute(v.aval)}")
    env[v] = x if type(x) is Var else x.val

  _check_jaxpr(ctx_factory, call_jaxpr)

  invars, outvars = call_jaxpr.invars, call_jaxpr.outvars
  in_map : Dict[Var,  InDBIdx] = {v:  InDBIdx(i) for i, v in enumerate( invars)}
  out_map: Dict[Var, OutDBIdx] = {x: OutDBIdx(i) for i, x in enumerate(outvars)
                                  if type(x) is Var}
  out_avals = [x.aval for x in call_jaxpr.outvars]
  out_type = [a.update(shape=tuple(in_map.get(d, out_map.get(d))
                                   if type(d) is Var else d for d in a.shape))
              if type(a) is DShapedArray else a for a in out_avals]
  return out_type, call_jaxpr.effects
