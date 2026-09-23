def _unpack_tuple(f, n):
  def g(c, *args, **kwargs):
    t = f(c, *args, **kwargs)
    return (xops.GetTupleElement(t, i) for i in range(n))
  return g
