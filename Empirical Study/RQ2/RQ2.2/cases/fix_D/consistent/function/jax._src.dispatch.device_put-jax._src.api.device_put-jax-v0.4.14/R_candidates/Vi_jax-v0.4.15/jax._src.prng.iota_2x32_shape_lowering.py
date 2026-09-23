def iota_2x32_shape_lowering(ctx, *, shape):
  aval_out, _ = ctx.avals_out
  aval_u64 = core.ShapedArray(shape, np.dtype('uint64'))

  def _add(x: ir.Value, y: ir.Value) -> ir.Value:
    return mlir.hlo.AddOp(x, y).result

  def _mul(x: core.DimSize, y: ir.Value) -> ir.Value:
    if core.is_constant_dim(x):
      x_const = mlir.ir_constant(np.array(x, np.dtype('uint64')))
    else:
      x_const, = mlir.eval_dynamic_shape(ctx, (x,))
      x_const = hlo.ConvertOp(
          ir.RankedTensorType.get(
              (),
              mlir.dtype_to_ir_type(np.dtype('uint64'))), x_const).result
    x_bcast = mlir.broadcast_in_dim(ctx, x_const, aval_u64,
                                    broadcast_dimensions=[])
    return mlir.hlo.MulOp(x_bcast, y).result

  assert len(shape) > 0

  iotas = [mlir.iota(ctx, aval_u64, dimension=dimension)
           for dimension in range(len(shape))]
  counts = bcast_iotas_to_reshaped_iota(_add, _mul, shape, iotas)
  shift = mlir.ir_constant(np.array(32, np.dtype('uint64')))
  shift = mlir.broadcast_in_dim(ctx, shift, aval_u64,
                                broadcast_dimensions=[])
  counts_shifted = mlir.hlo.ShiftRightLogicalOp(counts, shift).result
  counts_lo = mlir.hlo.ConvertOp(mlir.aval_to_ir_type(aval_out), counts).result
  counts_hi = mlir.hlo.ConvertOp(mlir.aval_to_ir_type(aval_out),
                                  counts_shifted).result
  return counts_hi, counts_lo
