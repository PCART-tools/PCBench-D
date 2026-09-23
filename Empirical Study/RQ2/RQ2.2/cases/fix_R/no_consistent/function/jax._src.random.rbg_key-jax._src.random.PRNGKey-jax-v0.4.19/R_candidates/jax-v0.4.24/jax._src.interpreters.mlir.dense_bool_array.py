def dense_bool_array(xs: Sequence[bool]) -> ir.DenseElementsAttr | ir.DenseBoolArrayAttr:
  # TODO: b/321794305 - remove this check when jaxlib is on StableHLO API v6 or higher
  if hlo.get_api_version() < 6 or xc.mlir_api_version < 55:
    return dense_bool_elements(xs)
  return ir.DenseBoolArrayAttr.get(xs)
