def _reduce_window_lower(
    reduce_op, init_value, ctx, operand, *,
    window_dimensions, window_strides, padding, base_dilation, window_dilation):
  aval_out, = ctx.avals_out
  operand_aval, = ctx.avals_in
  scalar_aval = operand_aval.update(shape=())
  scalar_type = mlir.aval_to_ir_type(scalar_aval)
  if any(not core.is_constant_shape(s)
         for s in [window_dimensions, window_dilation, window_strides, base_dilation, *padding]):
    raise NotImplementedError("ReduceWindowOp for dynamic shapes")
  rw = hlo.ReduceWindowOp(
      mlir.aval_to_ir_types(aval_out), [operand],
      [mlir.full_like_aval(ctx, init_value(scalar_aval.dtype), scalar_aval)],
      mlir.dense_int_elements(window_dimensions),
      window_strides=mlir.dense_int_elements(window_strides),
      base_dilations=mlir.dense_int_elements(base_dilation),
      window_dilations=mlir.dense_int_elements(window_dilation),
      padding=ir.DenseIntElementsAttr.get(np.asarray(padding, np.int64),
                                          shape=(len(padding), 2)))
  reducer = rw.regions[0].blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(reducer):
    hlo.ReturnOp(reduce_op(*reducer.arguments))
  return rw.results
