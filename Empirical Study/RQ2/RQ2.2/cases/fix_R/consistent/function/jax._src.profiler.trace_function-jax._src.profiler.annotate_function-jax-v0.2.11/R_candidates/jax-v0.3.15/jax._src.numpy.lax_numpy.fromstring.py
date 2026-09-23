@_wraps(np.fromstring)
def fromstring(string, dtype=float, count=-1, *, sep):
  return asarray(np.fromstring(string=string, dtype=dtype, count=count, sep=sep))
