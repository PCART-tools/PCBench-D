  @property
  def is_fully_addressable(self) -> bool:
    # Speed up `is_fully_addressable` since there is a high chance that the
    # mesh across multiple NamedSharding objects will be the same.
    return not self.mesh.is_multi_process
