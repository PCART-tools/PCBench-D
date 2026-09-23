def pure_callback_lowering(ctx, *args, callback, **params):

  def _callback(*flat_args):
    return tuple(pure_callback_impl(*flat_args, callback=callback, **params))

  sharding = None
  axis_context = ctx.module_context.axis_context
  if isinstance(axis_context, mlir.ShardingContext):
    if len(axis_context.device_assignment) > 1:
      raise NotImplementedError(
          "pure_callback is only supported in spmd computations when all mesh"
          " axes are partitioned manually (no partial automatic sharding)."
      )
  if isinstance(axis_context, mlir.SPMDAxisContext):
    if axis_context.manual_axes != frozenset(axis_context.mesh.axis_names):
      raise NotImplementedError(
          "pure_callback is only supported in spmd computations when all mesh"
          " axes are partitioned manually (no partial automatic sharding)."
      )
    sharding = xc.OpSharding()
    sharding.type = xc.OpSharding.Type.MANUAL

  result, _, keepalive = mlir.emit_python_callback(
      ctx, _callback, None, list(args), ctx.avals_in, ctx.avals_out, False,
      sharding=sharding)
  ctx.module_context.add_keepalive(keepalive)
  return result
