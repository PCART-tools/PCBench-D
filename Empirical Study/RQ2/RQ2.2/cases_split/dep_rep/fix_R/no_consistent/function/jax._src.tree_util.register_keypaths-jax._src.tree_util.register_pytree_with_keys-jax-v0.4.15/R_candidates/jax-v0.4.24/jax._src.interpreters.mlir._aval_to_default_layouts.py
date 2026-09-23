def _aval_to_default_layouts(aval):
  avals = [core.physical_aval(aval)]
  # Row major order is default for `NumPy`.
  return [list(range(aval.ndim - 1, -1, -1)) for aval in avals]
