  def __iter__(self):
    if self.ndim == 0:
      raise TypeError("iteration over a 0-d array")  # same as numpy error
    else:
      return (sl for chunk in self._chunk_iter(100) for sl in chunk._unstack())
