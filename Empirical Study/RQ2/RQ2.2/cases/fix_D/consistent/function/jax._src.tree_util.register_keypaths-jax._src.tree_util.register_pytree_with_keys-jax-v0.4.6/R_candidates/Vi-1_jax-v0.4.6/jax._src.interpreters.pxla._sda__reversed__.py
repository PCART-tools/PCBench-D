def _sda__reversed__(self):
  if self.ndim == 0:
    raise TypeError("iteration over a 0-d array")  # same as numpy error
  else:
    return (self[i] for i in range(self.shape[0] - 1, -1, -1))
