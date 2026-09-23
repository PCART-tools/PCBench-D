def _int(aval):
  return not aval.shape and issubdtype(aval.dtype, integer)
