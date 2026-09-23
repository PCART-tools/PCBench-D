def _canonicalize_value(a: np.generic | np.ndarray | int | float | ir.Value,
                        dtype: np.dtype | None = None) -> ir.Value:
  # TODO(sharadmv): use this function in most lowering rules and allow some
  # rules to opt out.
  if isinstance(a, ir.Value):
    return a
  mlir_type = None
  if dtype is not None:
    mlir_type = mlir.dtype_to_ir_type(dtype)
  return ir_constant(a, mlir_type=mlir_type)
