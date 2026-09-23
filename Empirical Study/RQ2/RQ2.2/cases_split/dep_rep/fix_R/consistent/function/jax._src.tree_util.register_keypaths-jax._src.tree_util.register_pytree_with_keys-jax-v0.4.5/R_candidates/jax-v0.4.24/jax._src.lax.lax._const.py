def _const(example, val):
  dtype = _dtype(example)
  if dtypes.is_python_scalar(example):
    val = dtypes.scalar_type_of(example)(val)
    return val if dtype == _dtype(val) else np.array(val, dtype)
  return np.array(val, dtype)
