def is_python_scalar(val):
  return not isinstance(val, np.generic) and isinstance(val, (bool, int, float, complex))
