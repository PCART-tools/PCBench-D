def _eval_jaxpr_discharge_state(jaxpr: core.Jaxpr, consts: Sequence[Any],
                                *args: Any):
  env: Dict[core.Var, Any] = {}

  def read(v: core.Atom) -> Any:
    if type(v) is core.Literal:
      return v.val
    assert isinstance(v, core.Var)
    return env[v]

  def write(v: core.Var, val: Any) -> None:
    env[v] = val

  map(write, jaxpr.constvars, consts)
  # Here some args may correspond to `Ref` avals but they'll be treated like
  # regular values in this interpreter.
  map(write, jaxpr.invars, args)

  for eqn in jaxpr.eqns:
    in_vals = map(read, eqn.invars)
    if eqn.primitive is get_p:
       # `y <- x[i]` becomes `y = ds x i`
      x, *idx = in_vals
      write(eqn.outvars[0], _dynamic_index(x, idx))
    elif eqn.primitive is swap_p:
      # `z, x[i] <- x[i], val` becomes:
      #    z = ds x i
      #    x = dus x i val
      x, val, *idx = in_vals
      write(eqn.outvars[0], _dynamic_index(x, idx))
      assert isinstance(eqn.invars[0], core.Var)
      write(eqn.invars[0], _dynamic_update_index(x, idx, val))
    elif eqn.primitive is addupdate_p:
      # `x[i] += val` becomes:
      #    y = ds x i
      #    z = y + val
      #    x = dus x i z
      x, val, *idx = in_vals
      ans = _dynamic_update_index(x, idx, val + _dynamic_index(x, idx))
      assert isinstance(eqn.invars[0], core.Var)
      write(eqn.invars[0], ans)
    else:
      # Default primitive rule, similar to `core.eval_jaxpr`. Note that here
      # we assume any higher-order primitives inside of the jaxpr are *not*
      # stateful.
      subfuns, bind_params = eqn.primitive.get_bind_params(eqn.params)
      ans = eqn.primitive.bind(*subfuns, *map(read, eqn.invars), **bind_params)
      if eqn.primitive.multiple_results:
        map(write, eqn.outvars, ans)
      else:
        write(eqn.outvars[0], ans)
  # By convention, we return the outputs of the jaxpr first and then the final
  # values of the `Ref`s. Callers to this function should be able to split
  # them up by looking at `len(jaxpr.outvars)`.
  out_vals = map(read, jaxpr.outvars)
  ref_vals = map(
      read, [v for v in jaxpr.invars if type(v.aval) is ShapedArrayRef])
  return out_vals + ref_vals
