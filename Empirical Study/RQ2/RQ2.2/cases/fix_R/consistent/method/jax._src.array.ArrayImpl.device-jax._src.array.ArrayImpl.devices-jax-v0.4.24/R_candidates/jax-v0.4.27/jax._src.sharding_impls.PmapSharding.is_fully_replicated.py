  @functools.cached_property
  def is_fully_replicated(self) -> bool:
    for s in self.sharding_spec.sharding:
      if isinstance(s, (sharding_specs.Unstacked, sharding_specs.Chunked)):
        return False
    return True
