  def __array__(self, dtype=None, context=None, copy=None):
    # copy argument is supported by np.asarray starting in numpy 2.0
    kwds = {} if copy is None else {'copy': copy}
    return np.asarray(self._value, dtype=dtype, **kwds)
