def dense_int_array(xs) -> ir.DenseIntElementsAttr | ir.DenseI64ArrayAttr:
  # TODO: b/321794305 - remove this check when jaxlib is on StableHLO API v5 or higher
  if hlo.get_api_version() < 5:
    return dense_int_elements(xs)
  return ir.DenseI64ArrayAttr.get(np.asarray(xs, np.int64))
