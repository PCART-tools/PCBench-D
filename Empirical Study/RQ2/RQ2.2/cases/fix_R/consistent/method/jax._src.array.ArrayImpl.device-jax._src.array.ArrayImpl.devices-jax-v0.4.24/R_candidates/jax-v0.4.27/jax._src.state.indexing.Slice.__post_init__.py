  def __post_init__(self):
    if self.stride < 1:
      raise ValueError("`stride` must be >= 1.")
