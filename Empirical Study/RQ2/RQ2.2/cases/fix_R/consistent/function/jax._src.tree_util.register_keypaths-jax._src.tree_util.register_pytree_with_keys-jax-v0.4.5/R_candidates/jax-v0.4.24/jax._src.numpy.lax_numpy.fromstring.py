@util.implements(np.fromstring)
def fromstring(string: str, dtype: DTypeLike = float, count: int = -1, *, sep: str) -> Array:
  return asarray(np.fromstring(string=string, dtype=dtype, count=count, sep=sep))
