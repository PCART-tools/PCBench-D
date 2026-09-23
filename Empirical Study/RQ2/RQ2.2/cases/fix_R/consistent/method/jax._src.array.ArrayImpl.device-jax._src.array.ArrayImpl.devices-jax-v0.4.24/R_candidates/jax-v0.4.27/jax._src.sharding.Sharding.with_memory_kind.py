  def with_memory_kind(self, kind: str) -> Sharding:
    """Returns a new Sharding instance with the specified memory kind."""
    raise NotImplementedError('Subclasses should implement this method')
