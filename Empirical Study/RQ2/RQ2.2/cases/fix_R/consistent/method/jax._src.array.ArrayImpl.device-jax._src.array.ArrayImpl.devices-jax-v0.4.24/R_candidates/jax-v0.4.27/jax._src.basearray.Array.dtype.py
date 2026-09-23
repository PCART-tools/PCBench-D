  @property
  @abc.abstractmethod
  def dtype(self) -> np.dtype:
    """The data type (:class:`numpy.dtype`) of the array."""
