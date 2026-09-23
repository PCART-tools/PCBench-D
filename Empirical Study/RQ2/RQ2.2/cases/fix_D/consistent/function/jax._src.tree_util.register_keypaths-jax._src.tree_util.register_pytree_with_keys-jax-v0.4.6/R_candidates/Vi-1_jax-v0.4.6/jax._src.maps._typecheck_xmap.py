def _typecheck_xmap(
    *in_atoms, call_jaxpr, name, in_axes, out_axes, donated_invars,
    global_axis_sizes, axis_resources, resource_env, backend,
    spmd_in_axes, spmd_out_axes, in_positional_semantics,
    out_positional_semantics):
  in_avals = [x.aval for x in in_atoms]
  axis_resource_count = _get_axis_resource_count(
      axis_resources, resource_env, in_positional_semantics)
  local_axis_sizes = {
      axis: axis_resource_count[axis].to_local(out_positional_semantics, global_size)
      for axis, global_size in global_axis_sizes.items()
  }
  binder_in_avals = [_insert_aval_axes(v.aval, a_in_axes, local_axis_sizes)
                     for v, a_in_axes in zip(call_jaxpr.invars, in_axes)]
  for binder_in_aval, in_aval in zip(binder_in_avals, in_avals):
    if not core.typecompat(binder_in_aval, in_aval):
      raise core.JaxprTypeError(
        f"xmap passes operand {in_aval} to jaxpr expecting {binder_in_aval}")

  with core.extend_axis_env_nd(global_axis_sizes.items()):
    core._check_jaxpr(lambda: core.JaxprPpContext(), call_jaxpr)

  mapped_out_avals = [v.aval for v in call_jaxpr.outvars]
  out_avals = [_insert_aval_axes(a, a_out_axes, local_axis_sizes)
               for a, a_out_axes in zip(mapped_out_avals, out_axes)]
  return out_avals, call_jaxpr.effects
