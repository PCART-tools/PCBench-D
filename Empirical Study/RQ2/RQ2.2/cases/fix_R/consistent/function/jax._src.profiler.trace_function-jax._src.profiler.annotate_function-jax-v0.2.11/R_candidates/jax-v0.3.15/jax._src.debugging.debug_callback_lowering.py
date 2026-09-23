def debug_callback_lowering(ctx, *args, effect, callback, **params):

  def _callback(*flat_args):
    return tuple(
        debug_callback_p.impl(
            *flat_args, effect=effect, callback=callback, **params))
  if effect in core.ordered_effects:
    token = ctx.tokens_in.get(effect)[0]
    result, token, keepalive = mlir.emit_python_callback(
        ctx, _callback, token, list(args), ctx.avals_in, ctx.avals_out, True)
    ctx.set_tokens_out(mlir.TokenSet({effect: (token,)}))
  else:
    result, token, keepalive = mlir.emit_python_callback(
        ctx, _callback, None, list(args), ctx.avals_in, ctx.avals_out, True)
  ctx.module_context.add_keepalive(keepalive)
  return result
