def _eval_jaxpr_discharge_state(
    jaxpr: core.Jaxpr, should_discharge: Sequence[bool], consts: Sequence[Any],
    *args: Any):
  env = Environment({})

  map(env.write, jaxpr.constvars, consts)
  # Here some args may correspond to `Ref` avals but they'll be treated like
  # regular values in this interpreter.
  map(env.write, jaxpr.invars, args)

  refs_to_discharge = {id(v.aval) for v, d
                          in zip(jaxpr.invars, should_discharge) if d
                          and isinstance(v.aval, AbstractRef)}

  for eqn in jaxpr.eqns:
    if _has_refs(eqn) and any(id(v.aval) in refs_to_discharge
                              for v in eqn.invars):
      if eqn.primitive not in _discharge_rules:
        raise NotImplementedError("No state discharge rule implemented for "
            f"primitive: {eqn.primitive}")
      invals = map(env.read, eqn.invars)
      in_avals = [v.aval for v in eqn.invars]
      out_avals = [v.aval for v in eqn.outvars]
      new_invals, ans = _discharge_rules[eqn.primitive](
          in_avals, out_avals, *invals, **eqn.params)
      for new_inval, invar in zip(new_invals, eqn.invars):
        if new_inval is not None:
          env.write(invar, new_inval)  # type: ignore[arg-type]
    else:
      # Default primitive rule, similar to `core.eval_jaxpr`. Note that here
      # we assume any higher-order primitives inside of the jaxpr are *not*
      # stateful.
      subfuns, bind_params = eqn.primitive.get_bind_params(eqn.params)
      ans = eqn.primitive.bind(*subfuns, *map(env.read, eqn.invars),
                               **bind_params)
    if eqn.primitive.multiple_results:
      map(env.write, eqn.outvars, ans)
    else:
      env.write(eqn.outvars[0], ans)
  # By convention, we return the outputs of the jaxpr first and then the final
  # values of the `Ref`s. Callers to this function should be able to split
  # them up by looking at `len(jaxpr.outvars)`.
  out_vals = map(env.read, jaxpr.outvars)
  ref_vals = map(
      env.read, [v for v in jaxpr.invars if id(v.aval) in refs_to_discharge])
  return out_vals + ref_vals
