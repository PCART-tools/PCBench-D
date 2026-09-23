def _householder_product_abstract_eval(a, taus):
  if not isinstance(a, ShapedArray) or not isinstance(taus, ShapedArray):
    raise NotImplementedError("Unsupported aval in householder_product_abstract_eval: "
                              f"{a.aval} {taus.aval}")
  if a.ndim < 2:
    raise ValueError("Argument to Householder product must have ndims >= 2")
  *batch_dims, m, n = a.shape
  *taus_batch_dims, k = taus.shape
  if a.dtype != taus.dtype or batch_dims != taus_batch_dims or k > min(m, n):
    raise ValueError(f"Type mismatch for Householder product: {a=} {taus=}")
  if m < n:
    raise ValueError("Householder product inputs must have at least as many "
                     f"rows as columns, got shape {a.shape}")
  return a
