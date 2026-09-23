def _numpy_array_constant(x: np.ndarray) -> Sequence[ir.Value]:
  element_type = dtype_to_ir_type(x.dtype)
  shape = x.shape
  if x.dtype == np.bool_:
    x = np.packbits(x, bitorder='little')
  x = np.ascontiguousarray(x)
  attr = ir.DenseElementsAttr.get(x, type=element_type, shape=shape)
  return (hlo.ConstantOp(attr).result,)
