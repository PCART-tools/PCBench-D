  @functools.cached_property
  def is_fully_replicated(self) -> bool:
    return self.shape == (1,) * self.ndim
