def _bcast(x, y, x_aval, y_aval, out_aval):
  if isinstance(x, (np.ndarray, np.uint32, int, float)):
    if hasattr(y, "type") and y.type == ir.IndexType.get():
      mlir_type = y.type
    else:
      mlir_type = mlir.dtype_to_ir_type(x_aval.dtype)
    x = ir_constant(x, mlir_type)
  if isinstance(y, (np.ndarray, np.uint32, int, float)):
    if hasattr(x, "type") and x.type == ir.IndexType.get():
      mlir_type = x.type
    else:
      mlir_type = mlir.dtype_to_ir_type(y_aval.dtype)
    y = ir_constant(y, mlir_type)
  out_shape = out_aval.shape
  bcast_shape = ir.VectorType.get(
      list(out_shape), mlir.dtype_to_ir_type(out_aval.dtype)
  )
  if x_aval.shape != out_aval.shape:
    x = vector.BroadcastOp(bcast_shape, x)
  if y_aval.shape != out_aval.shape:
    y = vector.BroadcastOp(bcast_shape, y)
  return x, y
