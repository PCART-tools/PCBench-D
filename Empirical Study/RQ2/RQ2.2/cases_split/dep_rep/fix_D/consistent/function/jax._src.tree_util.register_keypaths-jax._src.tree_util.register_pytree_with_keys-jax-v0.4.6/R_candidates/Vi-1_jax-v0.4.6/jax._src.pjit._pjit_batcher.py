def _pjit_batcher(insert_axis, spmd_axis_name,
                  axis_size, axis_name, main_type,
                  vals_in, dims_in,
                  jaxpr, in_shardings, out_shardings,
                  resource_env, donated_invars, name, in_positional_semantics,
                  out_positional_semantics, keep_unused, inline):
  new_jaxpr, axes_out = batching.batch_jaxpr2(
      jaxpr, axis_size, dims_in, axis_name=axis_name,
      spmd_axis_name=spmd_axis_name, main_type=main_type)

  # `insert_axis` is set to True only for some `xmap` uses.
  new_parts = (axis_name,) if insert_axis else (
      () if spmd_axis_name is None else spmd_axis_name)

  if resource_env is not None:
    mesh = resource_env.physical_mesh
  else:
    mesh = None

  in_shardings = tuple(
      _pjit_batcher_for_sharding(i, axis_in, new_parts, mesh, aval.ndim)
      if axis_in is not None else i
      for axis_in, i, aval in zip(dims_in, in_shardings, new_jaxpr.in_avals))
  out_shardings = tuple(
      _pjit_batcher_for_sharding(o, axis_out, new_parts, mesh, aval.ndim)
      if axis_out is not None else o
      for axis_out, o, aval in zip(axes_out, out_shardings, new_jaxpr.out_avals))
  vals_out = pjit_p.bind(
    *vals_in,
    jaxpr=new_jaxpr,
    in_shardings=in_shardings,
    out_shardings=out_shardings,
    resource_env=resource_env,
    donated_invars=donated_invars,
    name=name,
    in_positional_semantics=in_positional_semantics,
    out_positional_semantics=out_positional_semantics,
    keep_unused=keep_unused,
    inline=inline)
  return vals_out, axes_out
