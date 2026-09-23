def _sharding_constraint_hlo_lowering(ctx, x_node, *, sharding,
                                      resource_env, unconstrained_dims):
  aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  axis_ctx = ctx.module_context.axis_context
  # axis_ctx and manual_axes is *only used with xmap* and xmap only works with
  # NamedSharding. So update the NamedSharding to have the manual axes.
  if isinstance(axis_ctx, sharding_impls.SPMDAxisContext):
    mesh = resource_env.physical_mesh
    parsed_pspec = parse_flatten_op_sharding(sharding._hlo_sharding, mesh)[0]
    if xla_extension_version >= 188:
      sharding = NamedSharding._from_parsed_pspec(
          mesh, parsed_pspec, _manual_axes=axis_ctx.manual_axes)
    else:
      mps = NamedSharding._from_parsed_pspec(mesh, parsed_pspec)
      sharding = GSPMDSharding(
          mps._device_assignment, mps._to_xla_hlo_sharding(aval.ndim, axis_ctx=axis_ctx))
  return [
      mlir.wrap_with_sharding_op(ctx,
          x_node, out_aval,
          sharding._to_xla_hlo_sharding(aval.ndim).to_proto(),
          unspecified_dims=unconstrained_dims)
  ]
