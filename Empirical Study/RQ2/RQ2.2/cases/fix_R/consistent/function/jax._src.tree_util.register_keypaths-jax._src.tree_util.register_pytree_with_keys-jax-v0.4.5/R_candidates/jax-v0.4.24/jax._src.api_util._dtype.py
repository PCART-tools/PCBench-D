def _dtype(x):
  try:
    return dtypes.result_type(x)
  except ValueError:
    return dtypes.result_type(getattr(x, 'dtype'))
