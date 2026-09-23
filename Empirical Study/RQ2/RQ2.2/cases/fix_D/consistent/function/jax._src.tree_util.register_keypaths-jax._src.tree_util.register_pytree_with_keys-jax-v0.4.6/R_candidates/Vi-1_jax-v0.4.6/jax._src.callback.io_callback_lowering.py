def io_callback_lowering(ctx, *args, callback, ordered, **params):

  def _callback(*flat_args):
    return tuple(io_callback_impl(*flat_args, callback=callback,
                                  ordered=ordered, **params))

  # TODO(sharadmv): figure out the best API for sharding callbacks. For now, we
  # can only safely maximally shard. Should we allow device_index to be passed
  # in like host_callback?
  if isinstance(ctx.module_context.axis_context,
                (mlir.SPMDAxisContext, mlir.ShardingContext)):
    # Apply maximal sharding so pjit only executes the callback on device 0.
    sharding = xc.OpSharding()
    sharding.type = xc.OpSharding.Type.MAXIMAL
    sharding.tile_assignment_dimensions = [1]
    sharding.tile_assignment_devices = [0]
  else:
    sharding = None

  if ordered:
    token = ctx.tokens_in.get(_OrderedIOEffect)[0]
    result, token, keepalive = mlir.emit_python_callback(
        ctx, _callback, token, list(args), ctx.avals_in, ctx.avals_out, True,
        sharding=sharding)
    ctx.set_tokens_out(mlir.TokenSet({_OrderedIOEffect: (token,)}))
  else:
    result, token, keepalive = mlir.emit_python_callback(
        ctx, _callback, None, list(args), ctx.avals_in, ctx.avals_out, True,
        sharding=sharding)
  ctx.module_context.add_keepalive(keepalive)
  return result
