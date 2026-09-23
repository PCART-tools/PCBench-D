  @property
  def memory_kind(self) -> str | None:
    """Returns the memory kind of the sharding."""
    raise NotImplementedError('Subclasses should implement this method.')
