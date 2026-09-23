  @property
  @abc.abstractmethod
  def shape(self) -> tuple[int, ...]:
    """The shape of the array."""
