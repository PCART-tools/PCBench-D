  @property
  @abc.abstractmethod
  def addressable_shards(self) -> Sequence[Shard]:
    """List of addressable shards."""
