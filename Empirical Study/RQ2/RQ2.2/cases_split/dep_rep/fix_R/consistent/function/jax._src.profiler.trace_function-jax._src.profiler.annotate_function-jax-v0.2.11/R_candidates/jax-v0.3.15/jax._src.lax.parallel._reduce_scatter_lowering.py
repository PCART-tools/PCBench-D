def _reduce_scatter_lowering(prim, reducer, ctx, x,
                             *, scatter_dimension, axis_name,
                             axis_index_groups, axis_size, tiled):
  if ctx.module_context.platform in ("tpu", "cuda", "rocm"):
    x_aval, = ctx.avals_in
    aval_out, = ctx.avals_out
    scalar_aval = x_aval.update(shape=())
    replica_groups = _replica_groups(ctx.module_context.axis_env, axis_name,
                                     axis_index_groups)
    scatter_out_shape = list(x_aval.shape)
    scatter_out_shape[scatter_dimension] //= axis_size
    op = mhlo.ReduceScatterOp(
        mlir.aval_to_ir_type(x_aval.update(shape=scatter_out_shape)),
        x,
        scatter_dimension=mlir.i64_attr(scatter_dimension),
        replica_groups=_replica_groups_mhlo(replica_groups),
        channel_handle=None)
    scalar_type = mlir.aval_to_ir_type(scalar_aval)
    reducer_block = op.regions[0].blocks.append(scalar_type, scalar_type)
    with ir.InsertionPoint(reducer_block):
      lower_reducer = mlir.lower_fun(prim.bind, multiple_results=False)
      reducer_ctx = ctx.replace(primitive=None,
                                avals_in=[scalar_aval] * 2,
                                avals_out=[scalar_aval])
      out_nodes = lower_reducer(
          reducer_ctx, *([a] for a in reducer_block.arguments))
      mhlo.ReturnOp(util.flatten(out_nodes))

    if tiled:
      return op.results
    else:
      return mhlo.ReshapeOp(mlir.aval_to_ir_type(aval_out), op.result).results
  else:
    return mlir.lower_fun(_reduce_scatter_via_reducer, multiple_results=False)(
        ctx, x,
        reducer=reducer,
        scatter_dimension=scatter_dimension,
        axis_name=axis_name,
        axis_index_groups=axis_index_groups,
        axis_size=axis_size,
        tiled=tiled)
