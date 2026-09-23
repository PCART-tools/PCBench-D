  def __init__(self, fun: Callable):
    functools.update_wrapper(self, fun)
    self.fun = fun  # type: ignore[assignment]
