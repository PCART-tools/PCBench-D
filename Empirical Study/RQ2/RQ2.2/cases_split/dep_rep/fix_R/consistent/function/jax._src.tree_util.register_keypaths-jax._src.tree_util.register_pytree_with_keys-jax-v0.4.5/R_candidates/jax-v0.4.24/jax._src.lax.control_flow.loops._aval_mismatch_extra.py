def _aval_mismatch_extra(a1: core.AbstractValue, a2: core.AbstractValue) -> str:
  assert not core.typematch(a1, a2)
  if isinstance(a1, core.ShapedArray) and isinstance(a2, core.ShapedArray):
    dtype_mismatch = a1.dtype != a2.dtype
    shape_mismatch = a1.shape != a2.shape
    return (', so ' * (dtype_mismatch or shape_mismatch) +
            'the dtypes do not match' * dtype_mismatch +
            ' and also ' * (dtype_mismatch and shape_mismatch) +
            'the shapes do not match' * shape_mismatch)
  return ''
