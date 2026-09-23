  def __init__(self,
               fun: Callable[..., ReturnValue],
               nondiff_argnums: tuple[int, ...] = ()):
    update_wrapper(self, fun)
    self.fun = fun
    self.nondiff_argnums = nondiff_argnums
    self.fwd: Callable[..., tuple[ReturnValue, Any]] | None = None
    self.bwd: Callable[..., tuple[Any, ...]] | None = None
    self.symbolic_zeros = False
