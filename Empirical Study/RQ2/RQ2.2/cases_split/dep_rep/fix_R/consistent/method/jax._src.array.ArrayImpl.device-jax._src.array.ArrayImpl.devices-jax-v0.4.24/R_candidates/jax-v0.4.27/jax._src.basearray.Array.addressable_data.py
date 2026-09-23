  @abc.abstractmethod
  def addressable_data(self, index: int) -> Array:
    """Return an array of the addressable data at a particular index."""
