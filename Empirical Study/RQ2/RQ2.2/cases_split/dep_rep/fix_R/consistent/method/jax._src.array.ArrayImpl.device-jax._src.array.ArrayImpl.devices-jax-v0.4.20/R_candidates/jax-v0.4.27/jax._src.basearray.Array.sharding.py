  @property
  @abc.abstractmethod
  def sharding(self) -> Sharding:
    """The sharding for the array."""
