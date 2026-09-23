  @property
  def single(self) -> bool:
    """Whether this instance represents a single rotation."""
    return self.quat.ndim == 1
