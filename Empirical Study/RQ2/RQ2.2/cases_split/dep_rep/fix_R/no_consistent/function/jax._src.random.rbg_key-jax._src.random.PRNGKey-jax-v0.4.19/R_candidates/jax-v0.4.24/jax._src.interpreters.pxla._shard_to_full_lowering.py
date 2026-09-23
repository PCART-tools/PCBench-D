@partial(mlir.register_lowering, shard_to_full_p)
def _shard_to_full_lowering(ctx: mlir.LoweringRuleContext, x, *, axes: ArrayMapping, mesh: Mesh,
                            manual_axes: frozenset[sharding_impls.MeshAxisName]):
  aval_in, = ctx.avals_in
  aval_out, = ctx.avals_out
  proto = manual_proto(aval_in, manual_axes, mesh)  # type: ignore
  unspecified_dims = set(range(aval_in.ndim)) - set(axes.values())  # type: ignore
  sx = mlir.wrap_with_sharding_op(ctx, x, aval_in, proto,
                                  unspecified_dims=unspecified_dims)
  sharding_proto = (
      sharding_impls.NamedSharding(mesh, array_mapping_to_axis_resources(axes))
      ._to_xla_hlo_sharding(aval_out.ndim).to_proto())
  return (mlir.wrap_with_shard_to_full_op(ctx, sx, aval_out, sharding_proto,
                                          unspecified_dims),)
