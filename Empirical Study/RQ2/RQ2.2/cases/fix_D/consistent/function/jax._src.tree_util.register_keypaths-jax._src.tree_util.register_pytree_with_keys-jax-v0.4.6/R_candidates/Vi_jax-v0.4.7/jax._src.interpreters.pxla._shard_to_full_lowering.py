@partial(mlir.register_lowering, shard_to_full_p)
def _shard_to_full_lowering(ctx, x, *, axes: ArrayMapping, mesh: Mesh,
                            manual_axes: FrozenSet[mesh.MeshAxisName]):
  aval_in, = ctx.avals_in
  aval_out, = ctx.avals_out
  proto = manual_proto(aval_in, manual_axes, mesh)
  result_type, = mlir.aval_to_ir_types(aval_out)
  unspecified_dims = set(range(aval_in.ndim)) - set(axes.values())
  sx = mlir.wrap_with_sharding_op(x, proto, unspecified_dims=unspecified_dims)
  sharding_proto = mesh_sharding_specs(mesh.shape, mesh.axis_names)(aval_out, axes).sharding_proto()
  return mlir.wrap_with_shard_to_full_op(result_type, sx, sharding_proto, unspecified_dims),
