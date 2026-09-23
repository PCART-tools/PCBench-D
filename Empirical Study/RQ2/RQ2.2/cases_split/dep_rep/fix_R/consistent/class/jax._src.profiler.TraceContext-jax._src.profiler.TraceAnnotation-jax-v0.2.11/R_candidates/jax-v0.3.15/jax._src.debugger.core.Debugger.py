class Debugger(Protocol):

  def __call__(self, frames: List[DebuggerFrame], thread_id: Optional[int],
      **kwargs: Any) -> None:
    ...
