class EventListenerWithMetadata(Protocol):

  def __call__(self, event: str, **kwargs: str | int) -> None:
    ...
