def _sharding_constraint_hlo_lowering(ctx, x_node, *, sharding,
                                      resource_env, unconstrained_dims):
  aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  axis_ctx = ctx.module_context.axis_context
  # axis_ctx and manual_axes is *only used with xmap* and xmap only works with
  # NamedSharding. So convert the GSPMDSharding to NamedSharding
  # and then convert it back with the added special axes.
  if isinstance(axis_ctx, sharding_impls.SPMDAxisContext):
    mesh = resource_env.physical_mesh
    parsed_pspec = parse_flatten_op_sharding(sharding._hlo_sharding, mesh)[0]
    mps = NamedSharding._from_parsed_pspec(mesh, parsed_pspec)
    sharding = GSPMDSharding(
        mps._device_assignment, mps._to_xla_hlo_sharding(aval.ndim, axis_ctx=axis_ctx))
  return [
      mlir.wrap_with_sharding_op(ctx,
          x_node, out_aval,
          sharding._to_xla_hlo_sharding(aval.ndim).to_proto(),
          unspecified_dims=unconstrained_dims)
  ]
