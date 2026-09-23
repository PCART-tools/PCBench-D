  @property
  @abc.abstractmethod
  def global_shards(self) -> Sequence[Shard]:
    """List of global shards."""
