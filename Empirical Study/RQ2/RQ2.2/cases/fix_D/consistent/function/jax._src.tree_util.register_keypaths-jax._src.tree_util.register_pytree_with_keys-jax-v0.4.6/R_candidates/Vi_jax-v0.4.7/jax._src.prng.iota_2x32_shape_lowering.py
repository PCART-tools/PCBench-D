def iota_2x32_shape_lowering(ctx, *, shape):
  def _add(x, y):
    return mlir.hlo.AddOp(x, y).result

  def _mul(x, y):
    x_const = mlir.ir_constant(np.array(x, np.dtype('uint64')),
                               canonicalize_types=False)
    x_bcast = mlir.hlo.BroadcastOp(x_const, mlir.dense_int_elements(shape))
    return mlir.hlo.MulOp(x_bcast, y).result

  assert len(shape) > 0
  aval_out, _ = ctx.avals_out
  aval_u64 = core.ShapedArray(shape, np.dtype('uint64'))
  iotas = [mlir.hlo.IotaOp(mlir.aval_to_ir_type(aval_u64),
                            mlir.i64_attr(dimension)).result
           for dimension in range(len(shape))]
  counts = bcast_iotas_to_reshaped_iota(_add, _mul, shape, iotas)
  shift = mlir.ir_constant(np.array(32, np.dtype('uint64')),
                           canonicalize_types=False)
  shift = mlir.hlo.BroadcastOp(shift, mlir.dense_int_elements(shape)).result
  counts_shifted = mlir.hlo.ShiftRightLogicalOp(counts, shift).result
  counts_lo = mlir.hlo.ConvertOp(mlir.aval_to_ir_type(aval_out), counts).result
  counts_hi = mlir.hlo.ConvertOp(mlir.aval_to_ir_type(aval_out),
                                  counts_shifted).result
  return counts_hi, counts_lo
