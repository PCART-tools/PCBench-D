  def __len__(self):
    if self.ndim == 0: raise TypeError('len() of unsized object')
    return self.shape[0]
