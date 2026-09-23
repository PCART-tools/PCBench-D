def check_lowering_rule(ctx, *args, err_tree, debug):
  if debug:
    # NOOP (check will only trigger when discharged)
    return []
  if not config.jax_experimental_unsafe_xla_runtime_errors:
    raise functionalization_error

  out_op, _, keep_alive = mlir.emit_python_callback(
      ctx, callback=functools.partial(python_err, err_tree),
      token=None,
      operands=args,
      operand_avals=list(ctx.avals_in),
      result_avals=list(ctx.avals_out),
      has_side_effect=True)
  ctx.module_context.add_keepalive(keep_alive)
  return out_op
