def _generic_reduce_window_lower(ctx, *args, jaxpr, consts,
                                 window_dimensions, window_strides, padding,
                                 base_dilation, window_dilation):
  operands, init_values = util.split_list(args, [len(args) // 2])
  _, init_value_avals = util.split_list(ctx.avals_in, [len(operands)])

  def reducer_body(reducer: ir.Block) -> Sequence[ir.Value]:
    if jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `reduce_window`.')
    out_nodes, _ = mlir.jaxpr_subcomp(ctx.module_context, jaxpr,
        mlir.TokenSet(), consts, *([a] for a in reducer.arguments),
        dim_var_values=ctx.dim_var_values)
    return util.flatten(out_nodes)

  return mlir.reduce_window(
      ctx,
      reducer_name="generic_reduce_window_reducer",
      reducer_body=reducer_body,
      operands=operands,
      init_values=init_values, init_values_avals=init_value_avals,
      out_avals=ctx.avals_out,
      window_dimensions=window_dimensions, window_strides=window_strides,
      base_dilation=base_dilation, window_dilation=window_dilation,
      padding=padding)
