def _bcast(x, y, x_aval, y_aval, out_aval):
  if isinstance(x, (np.ndarray, np.number, int, float)):
    if hasattr(y, "type") and y.type == ir.IndexType.get():
      mlir_type = y.type
    else:
      mlir_type = _dtype_to_ir_type(x_aval.dtype)
    x = ir_constant(x, mlir_type)
  if isinstance(y, (np.ndarray, np.number, int, float)):
    if hasattr(x, "type") and x.type == ir.IndexType.get():
      mlir_type = x.type
    else:
      mlir_type = _dtype_to_ir_type(y_aval.dtype)
    y = ir_constant(y, mlir_type)
  out_shape = list(out_aval.shape)
  if x_aval.shape != out_aval.shape:
    x_ty = ir.VectorType.get(out_shape, _dtype_to_ir_type(x_aval.dtype))
    x = vector.BroadcastOp(x_ty, x)
  if y_aval.shape != out_aval.shape:
    y_ty = ir.VectorType.get(out_shape, _dtype_to_ir_type(y_aval.dtype))
    y = vector.BroadcastOp(y_ty, y)
  return x, y
