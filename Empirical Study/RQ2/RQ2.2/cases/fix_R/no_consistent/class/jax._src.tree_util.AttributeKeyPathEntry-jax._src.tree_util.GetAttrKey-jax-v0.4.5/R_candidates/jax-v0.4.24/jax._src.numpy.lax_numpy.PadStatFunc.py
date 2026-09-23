class PadStatFunc(Protocol):
  def __call__(self, array: ArrayLike, /, *,
               axis: int | None = None,
               keepdims: bool = False) -> Array: ...
