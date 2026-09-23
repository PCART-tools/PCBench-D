def _reduce_scatter_lowering(
    prim, ctx, x,
    *, scatter_dimension, axis_name,
    axis_index_groups, axis_size, tiled):
  x_aval, = ctx.avals_in
  aval_out, = ctx.avals_out
  scalar_aval = x_aval.update(shape=())
  replica_groups = _replica_groups(ctx.module_context.axis_env, axis_name,
                                   axis_index_groups)
  scatter_out_shape = list(x_aval.shape)
  scatter_out_shape[scatter_dimension] //= axis_size
  axis_context = ctx.module_context.axis_context
  is_spmd = isinstance(
      axis_context,
      (sharding_impls.SPMDAxisContext, sharding_impls.ShardingContext),
  )
  if is_spmd:
    # We want to emit the all-gather with global device IDs and a unique
    # channel ID, as otherwise it interprets the devices as replicas instead
    # of partitions - and XLA is configured with only a single replica.
    channel = ctx.module_context.new_channel()
    other_args = dict(
        channel_handle=hlo.ChannelHandle.get(
            channel, mlir.DEVICE_TO_DEVICE_TYPE),
        use_global_device_ids=ir.BoolAttr.get(True))
  else:
    other_args = {}
  op = hlo.ReduceScatterOp(
      mlir.aval_to_ir_type(x_aval.update(shape=scatter_out_shape)),
      x,
      scatter_dimension=mlir.i64_attr(scatter_dimension),
      replica_groups=_replica_groups_hlo(replica_groups),
      **other_args)
  scalar_type = mlir.aval_to_ir_type(scalar_aval)
  reducer_block = op.regions[0].blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(reducer_block):
    lower_reducer = mlir.lower_fun(prim.bind, multiple_results=False)
    reducer_ctx = ctx.replace(primitive=None,
                              avals_in=[scalar_aval] * 2,
                              avals_out=[scalar_aval])
    out_nodes = lower_reducer(
        reducer_ctx, *([a] for a in reducer_block.arguments))
    hlo.return_(util.flatten(out_nodes))

  if tiled:
    return op.results
  else:
    return [hlo.reshape(mlir.aval_to_ir_type(aval_out), op.result)]
