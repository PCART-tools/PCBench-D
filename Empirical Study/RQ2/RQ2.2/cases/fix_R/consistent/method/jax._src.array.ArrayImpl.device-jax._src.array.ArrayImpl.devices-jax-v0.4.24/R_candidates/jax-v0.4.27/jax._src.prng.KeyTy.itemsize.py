  @property
  def itemsize(self) -> int:
    return math.prod(self._impl.key_shape) * np.dtype('uint32').itemsize
