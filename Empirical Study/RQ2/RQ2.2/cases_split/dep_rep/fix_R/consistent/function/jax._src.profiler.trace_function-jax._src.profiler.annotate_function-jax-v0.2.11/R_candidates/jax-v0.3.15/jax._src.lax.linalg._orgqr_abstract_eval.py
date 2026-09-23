def _orgqr_abstract_eval(a, taus):
  if not isinstance(a, ShapedArray) or not isinstance(taus, ShapedArray):
    raise NotImplementedError("Unsupported aval in orgqr_abstract_eval: "
                              f"{a.aval} {taus.aval}")
  if a.ndim < 2:
    raise ValueError("Argument to QR decomposition must have ndims >= 2")
  *batch_dims, m, n = a.shape
  *taus_batch_dims, k = taus.shape
  if a.dtype != taus.dtype or batch_dims != taus_batch_dims or k > min(m, n):
    raise ValueError(f"Type mismatch for orgqr: a={a} taus={taus}")
  return a
