  @property
  @abc.abstractmethod
  def is_fully_replicated(self) -> bool:
    """Is this Array fully replicated?"""
