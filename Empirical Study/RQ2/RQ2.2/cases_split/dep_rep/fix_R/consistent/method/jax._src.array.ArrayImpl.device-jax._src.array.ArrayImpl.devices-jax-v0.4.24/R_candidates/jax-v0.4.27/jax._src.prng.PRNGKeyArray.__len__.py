  def __len__(self):
    if self._is_scalar():
      raise TypeError('len() of unsized object')
    return len(self._base_array)
