def _select_and_scatter_lower(
    ctx, operand, source, init_value, *, select_jaxpr,
    select_consts, scatter_jaxpr, scatter_consts, window_dimensions,
    window_strides, padding):
  operand_aval, source_aval, init_value_aval = ctx.avals_in
  aval_out, = ctx.avals_out
  scalar_aval = operand_aval.update(shape=())
  scalar_type = mlir.aval_to_ir_type(scalar_aval)
  op = hlo.SelectAndScatterOp(
      mlir.aval_to_ir_type(aval_out),
      operand,
      source,
      init_value,
      window_dimensions=mlir.dense_int_elements(window_dimensions),
      window_strides=mlir.dense_int_elements(window_strides),
      padding=ir.DenseIntElementsAttr.get(np.asarray(padding, np.int64),
                                          shape=(len(padding), 2)))
  select = op.select.blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(select):
    if select_jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `select`.')
    out_nodes, _ = mlir.jaxpr_subcomp(ctx.module_context, select_jaxpr,
                                      mlir.TokenSet(), select_consts,
                                      *([a] for a in select.arguments),
                                      dim_var_values=ctx.dim_var_values)
    hlo.ReturnOp(util.flatten(out_nodes))
  scatter = op.scatter.blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(scatter):
    if scatter_jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `scatter`.')
    out_nodes, _ = mlir.jaxpr_subcomp(ctx.module_context, scatter_jaxpr,
                                      mlir.TokenSet(), scatter_consts,
                                      *([a] for a in scatter.arguments),
                                      dim_var_values=ctx.dim_var_values)
    hlo.ReturnOp(util.flatten(out_nodes))
  return op.results
