def _all_gather_lowering(ctx, x, *, all_gather_dimension, axis_name,
                         axis_index_groups, axis_size, tiled):
  # TODO(jekbradbury): enable for all_gather_dimension > 0
  x_aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  if (ctx.module_context.platform == 'tpu' or
      ctx.module_context.platform in ('cuda', 'rocm')
      and all_gather_dimension == 0):
    if not tiled:
      new_shape = list(x_aval.shape)
      new_shape.insert(all_gather_dimension, 1)
      broadcast_dimensions = [i for i in range(len(new_shape)) if i != all_gather_dimension]
      x = mhlo.BroadcastInDimOp(
          mlir.aval_to_ir_type(x_aval.update(shape=new_shape)), x,
          mlir.dense_int_elements(broadcast_dimensions))
    replica_groups = _replica_groups(ctx.module_context.axis_env, axis_name,
                                     axis_index_groups)
    return mhlo.AllGatherOp(
        mlir.aval_to_ir_type(out_aval),
        x, all_gather_dim=mlir.i64_attr(all_gather_dimension),
        replica_groups=_replica_groups_mhlo(replica_groups),
        channel_handle=None).results
  else:
    lowering = mlir.lower_fun(_all_gather_via_psum, multiple_results=False)
    return lowering(
        ctx, x, all_gather_dimension=all_gather_dimension,
        axis_name=axis_name, axis_index_groups=axis_index_groups,
        axis_size=axis_size, tiled=tiled)
