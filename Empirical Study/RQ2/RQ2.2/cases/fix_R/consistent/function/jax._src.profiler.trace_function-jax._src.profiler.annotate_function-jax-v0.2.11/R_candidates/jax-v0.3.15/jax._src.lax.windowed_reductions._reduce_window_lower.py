def _reduce_window_lower(
    reduce_op, init_value, ctx, operand, *,
    window_dimensions, window_strides, padding, base_dilation, window_dilation):
  aval_out, = ctx.avals_out
  operand_aval, = ctx.avals_in
  scalar_aval = operand_aval.update(shape=())
  scalar_type = mlir.aval_to_ir_type(scalar_aval)
  rw = mhlo.ReduceWindowOp(
      mlir.aval_to_ir_types(aval_out), [operand],
      [mlir.full_like_aval(init_value(scalar_aval.dtype), scalar_aval)],
      mlir.dense_int_elements(window_dimensions),
      window_strides=mlir.dense_int_elements(window_strides),
      base_dilations=mlir.dense_int_elements(base_dilation),
      window_dilations=mlir.dense_int_elements(window_dilation),
      padding=ir.DenseIntElementsAttr.get(np.asarray(padding, np.int64),
                                          shape=(len(padding), 2)))
  reducer = rw.regions[0].blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(reducer):
    mhlo.ReturnOp(reduce_op(*reducer.arguments))
  return rw.results
