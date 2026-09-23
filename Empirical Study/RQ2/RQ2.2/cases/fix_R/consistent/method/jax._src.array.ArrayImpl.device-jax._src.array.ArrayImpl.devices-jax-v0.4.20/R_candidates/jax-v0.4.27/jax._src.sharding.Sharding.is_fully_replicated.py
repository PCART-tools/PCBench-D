  @property
  def is_fully_replicated(self) -> bool:
    """Is this sharding fully replicated?

    A sharding is fully replicated if each device has a complete copy of the
    entire data.
    """
    raise NotImplementedError('Subclasses should implement this method.')
