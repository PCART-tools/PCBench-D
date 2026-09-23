def _check_map(ctx_factory, prim, in_avals, params):
  if "call_jaxpr" not in params:
    raise JaxprTypeError(f"Map primitive {prim} missing 'call_jaxpr' parameter")
  call_jaxpr = params["call_jaxpr"]
  ordered_effects_ = effects.ordered_effects.filter_in(call_jaxpr.effects)
  if ordered_effects_:
    raise JaxprTypeError(
        f"Map primitive {prim} mapping ordered effects: {ordered_effects_}")
  if "axis_size" not in params:
    raise JaxprTypeError(f"Map primitive {prim} missing 'axis_size' parameter")
  axis_size = params["axis_size"]
  if "axis_name" not in params:
    raise JaxprTypeError(f"Map primitive {prim} missing 'axis_name' parameter")
  axis_name = params["axis_name"]
  if "in_axes" not in params:
    raise JaxprTypeError(f"Map primitive {prim} missing 'in_axes' parameter")
  in_axes = params["in_axes"]
  if "out_axes" not in params:
    raise JaxprTypeError(f"Map primitive {prim} missing 'out_axes' parameter")
  out_axes = params["out_axes"]

  binder_avals = [unmapped_aval(axis_size, axis_name, in_axis, v.aval)
                  if in_axis is not None else v.aval
                  for v, in_axis in zip(call_jaxpr.invars, in_axes)]
  for binder_aval, in_aval in zip(binder_avals, in_avals):
    if not typecompat(binder_aval, in_aval):
      raise JaxprTypeError(f"Call primitive {prim} passes operand {in_aval} "
                           f"to jaxpr expecting {binder_aval}")

  with extend_axis_env(params['axis_name'], axis_size, None):
    _check_jaxpr(ctx_factory, call_jaxpr)

  mapped_out_avals = [v.aval for v in call_jaxpr.outvars]
  out_avals = [unmapped_aval(axis_size, axis_name, out_axis, aval)
               if out_axis is not None else aval
               for aval, out_axis in zip(mapped_out_avals, out_axes)]
  return out_avals, call_jaxpr.effects
