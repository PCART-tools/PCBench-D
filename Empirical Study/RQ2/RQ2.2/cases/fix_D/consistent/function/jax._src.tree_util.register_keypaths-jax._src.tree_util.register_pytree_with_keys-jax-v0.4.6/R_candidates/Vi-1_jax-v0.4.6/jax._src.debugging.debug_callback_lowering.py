def debug_callback_lowering(ctx, *args, effect, callback, **params):

  axis_context = ctx.module_context.axis_context
  if (isinstance(axis_context, mlir.SPMDAxisContext) and
        set(axis_context.manual_axes) == set(axis_context.mesh.axis_names)):
    # If we have fully manual sharding during lowering, that means the JAX
    # program has per-device semantics, so we run the callback on each device.
    sharding = xc.OpSharding()
    sharding.type = xc.OpSharding.Type.MANUAL
  elif isinstance(axis_context, (mlir.ShardingContext, mlir.SPMDAxisContext)):
    # If we have fully automatic sharding during lowering, that means the JAX
    # program has bulk array semantics, so we run the callback with a MAXIMAL
    # sharding and hence execute it only once on the full logical value).
    # If we have partially automatic sharding, we do this too... not sure why!
    sharding = xc.OpSharding()
    sharding.type = xc.OpSharding.Type.MAXIMAL
    sharding.tile_assignment_dimensions = [1]
    sharding.tile_assignment_devices = [0]
  else:
    # When there's no SPMD partitioning going on, don't annotate a sharding.
    sharding = None

  def _callback(*flat_args):
    return tuple(
        debug_callback_p.impl(
            *flat_args, effect=effect, callback=callback, **params))
  if effects.ordered_effects.contains(effect):
    token = ctx.tokens_in.get(effect)[0]
    result, token, keepalive = mlir.emit_python_callback(
        ctx, _callback, token, list(args), ctx.avals_in, ctx.avals_out, True)
    ctx.set_tokens_out(mlir.TokenSet({effect: (token,)}))
  else:
    result, token, keepalive = mlir.emit_python_callback(
        ctx, _callback, None, list(args), ctx.avals_in, ctx.avals_out, True,
        sharding=sharding)
  ctx.module_context.add_keepalive(keepalive)
  return result
