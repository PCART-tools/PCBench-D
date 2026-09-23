  def __array__(self, dtype=None, context=None):
    return np.asarray(self._value, dtype=dtype)
