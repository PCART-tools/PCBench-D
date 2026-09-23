def _aval_to_default_layout(aval):
  # Row major order is default for `NumPy`.
  return list(range(aval.ndim - 1, -1, -1))
