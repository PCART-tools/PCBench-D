  def __init__(self,
               fun: Callable[..., ReturnValue],
               nondiff_argnums: tuple[int, ...] = (),
               ):
    update_wrapper(self, fun)
    self.fun = fun
    self.nondiff_argnums = nondiff_argnums
