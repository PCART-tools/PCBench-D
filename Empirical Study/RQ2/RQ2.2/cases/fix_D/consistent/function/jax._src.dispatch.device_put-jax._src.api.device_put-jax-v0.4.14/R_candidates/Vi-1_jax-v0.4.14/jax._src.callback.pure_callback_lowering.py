def pure_callback_lowering(ctx, *args, callback, **params):

  def _callback(*flat_args):
    return tuple(pure_callback_impl(*flat_args, callback=callback, **params))

  sharding = None
  axis_context = ctx.module_context.axis_context
  if isinstance(axis_context, sharding_impls.SPMDAxisContext):
    # If we have fully manual sharding during lowering, that means the JAX
    # program has per-device semantics, so we run the callback on each device.
    if axis_context.manual_axes != frozenset(axis_context.mesh.axis_names):
      raise NotImplementedError(
          "pure_callback is only supported in spmd computations when all mesh"
          " axes are partitioned manually (no partial automatic sharding)."
      )
    sharding = xc.OpSharding()
    sharding.type = xc.OpSharding.Type.MANUAL
  elif isinstance(axis_context, sharding_impls.ShardingContext):
    # If we have fully automatic sharding during lowering, that means the JAX
    # program has bulk array semantics, so we run the callback with a MAXIMAL
    # sharding and hence execute it only once on the full logical value).
    sharding = xc.OpSharding()
    sharding.type = xc.OpSharding.Type.MAXIMAL
    sharding.tile_assignment_dimensions = [1]
    sharding.tile_assignment_devices = [0]
  else:
    # When there's no SPMD partitioning going on, don't annotate a sharding.
    sharding = None
  if isinstance(axis_context, sharding_impls.SPMDAxisContext):
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
