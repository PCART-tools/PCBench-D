  def __iter__(self):
    if self.ndim == 0: raise TypeError('iteration over a 0-d array')
    raise NotImplementedError
