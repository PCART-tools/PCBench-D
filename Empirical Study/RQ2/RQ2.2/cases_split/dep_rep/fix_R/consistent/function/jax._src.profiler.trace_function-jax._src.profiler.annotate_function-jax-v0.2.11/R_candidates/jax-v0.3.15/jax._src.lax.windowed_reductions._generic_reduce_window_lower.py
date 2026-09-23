def _generic_reduce_window_lower(ctx, *args, jaxpr, consts,
                                 window_dimensions, window_strides, padding,
                                 base_dilation, window_dilation):
  operands, init_values = util.split_list(args, [len(args) // 2])
  _, init_value_avals = util.split_list(ctx.avals_in, [len(operands)])
  scalar_types = [mlir.aval_to_ir_type(aval) for aval in init_value_avals]
  rw = mhlo.ReduceWindowOp(
      map(mlir.aval_to_ir_type, ctx.avals_out),
      operands,
      init_values,
      mlir.dense_int_elements(window_dimensions),
      window_strides=mlir.dense_int_elements(window_strides),
      base_dilations=mlir.dense_int_elements(base_dilation),
      window_dilations=mlir.dense_int_elements(window_dilation),
      padding=ir.DenseIntElementsAttr.get(np.asarray(padding, np.int64),
                                          shape=(len(padding), 2)))
  reducer = rw.regions[0].blocks.append(*(scalar_types + scalar_types))
  with ir.InsertionPoint(reducer):
    if jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `reduce_window`.')
    out_nodes, _ = mlir.jaxpr_subcomp(ctx.module_context, jaxpr,
        mlir.TokenSet(), consts, *([a] for a in reducer.arguments))
    mhlo.ReturnOp(util.flatten(out_nodes))
  return rw.results
