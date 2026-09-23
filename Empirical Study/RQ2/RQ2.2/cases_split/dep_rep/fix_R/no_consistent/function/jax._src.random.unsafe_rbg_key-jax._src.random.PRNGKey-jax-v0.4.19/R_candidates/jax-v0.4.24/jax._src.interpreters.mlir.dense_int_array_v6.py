def dense_int_array_v6(xs) -> ir.DenseIntElementsAttr | ir.DenseI64ArrayAttr:
  if hlo.get_api_version() < 6 or xc.mlir_api_version < 55:
    return dense_int_elements(xs)
  return ir.DenseI64ArrayAttr.get(np.asarray(xs, np.int64))
