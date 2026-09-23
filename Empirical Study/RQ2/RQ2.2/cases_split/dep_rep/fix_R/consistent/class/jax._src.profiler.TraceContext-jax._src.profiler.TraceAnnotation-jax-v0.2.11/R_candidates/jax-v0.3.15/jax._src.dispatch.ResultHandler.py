  class ResultHandler(Protocol):
    def __call__(self, env: Optional[Sequence[Any]], *args: xla.Buffer) -> Any:
      """Boxes raw buffers into their user-facing representation."""
