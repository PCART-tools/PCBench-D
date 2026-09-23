@partial(mlir.register_lowering, full_to_shard_p)
def _full_to_shard_lowering(ctx, x, *, axes: ArrayMapping, mesh: Mesh, manual_axes: FrozenSet[MeshAxisName]):
  # TODO: Can we short-circuit for replicated values? Probably not.
  aval_in, = ctx.avals_in
  aval_out, = ctx.avals_out
  sharding_proto = mesh_sharding_specs(mesh.shape, mesh.axis_names)(aval_in, axes).sharding_proto()
  unspecified_dims = set(range(aval_in.ndim)) - set(axes.values())
  sx = mlir.wrap_with_sharding_op(x, sharding_proto, unspecified_dims=unspecified_dims)
  proto = manual_proto(aval_in, manual_axes, mesh)
  result_type, = mlir.aval_to_ir_types(aval_out)
  return mlir.wrap_with_full_to_shard_op(result_type, sx, proto, unspecified_dims=unspecified_dims),
