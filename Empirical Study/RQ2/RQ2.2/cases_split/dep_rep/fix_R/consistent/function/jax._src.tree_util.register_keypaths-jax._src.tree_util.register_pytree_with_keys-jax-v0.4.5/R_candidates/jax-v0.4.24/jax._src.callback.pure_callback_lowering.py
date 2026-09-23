def pure_callback_lowering(
    ctx, *args, callback, sharding: SingleDeviceSharding | None, **params
):
  def _callback(*flat_args):
    return tuple(
        pure_callback_impl(
            *flat_args,
            callback=callback,
            sharding=None,  # unused.
            **params,
        )
    )

  op_sharding = _callback_op_sharding(ctx.module_context.axis_context, sharding)
  result, _, _ = mlir.emit_python_callback(
      ctx,
      _callback,
      None,
      list(args),
      ctx.avals_in,
      ctx.avals_out,
      False,
      sharding=op_sharding,
  )
  return result
