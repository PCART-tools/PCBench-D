  def __repr__(self):
    return (f'Array({self.shape}, dtype={self.dtype.name}) overlaying:\n'
            f'{self._base_array}')
