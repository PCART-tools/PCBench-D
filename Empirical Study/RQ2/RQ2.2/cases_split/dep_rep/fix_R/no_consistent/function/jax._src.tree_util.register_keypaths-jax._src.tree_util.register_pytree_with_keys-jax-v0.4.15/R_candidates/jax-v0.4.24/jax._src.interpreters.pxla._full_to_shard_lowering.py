@partial(mlir.register_lowering, full_to_shard_p)
def _full_to_shard_lowering(ctx, x, *, axes: ArrayMapping, mesh: Mesh,
                            manual_axes: frozenset[sharding_impls.MeshAxisName]):
  # TODO: Can we short-circuit for replicated values? Probably not.
  aval_in, = ctx.avals_in
  aval_out, = ctx.avals_out
  sharding_proto = (
      sharding_impls.NamedSharding(mesh, array_mapping_to_axis_resources(axes))
      ._to_xla_hlo_sharding(aval_in.ndim).to_proto())
  unspecified_dims = set(range(aval_in.ndim)) - set(axes.values())
  sx = mlir.wrap_with_sharding_op(ctx, x, aval_in, sharding_proto,
                                  unspecified_dims=unspecified_dims)
  proto = manual_proto(aval_in, manual_axes, mesh)
  return (mlir.wrap_with_full_to_shard_op(ctx, sx, aval_out, proto,
                                          unspecified_dims=unspecified_dims),)
