def _result_dtype(op, *args):
  """Compute result dtype of applying op to arguments with given dtypes."""
  args = [np.ones((0,) * ndim(arg), _dtype(arg)) for arg in args]
  return _dtype(op(*args))
