def _item(a: Array) -> Any:
  """Copy an element of an array to a standard Python scalar and return it."""
  if dtypes.issubdtype(a.dtype, np.complexfloating):
    return complex(a)
  elif dtypes.issubdtype(a.dtype, np.floating):
    return float(a)
  elif dtypes.issubdtype(a.dtype, np.integer):
    return int(a)
  elif dtypes.issubdtype(a.dtype, np.bool_):
    return bool(a)
  else:
    raise TypeError(a.dtype)
