  def __hash__(self) -> int:
    # Do not include _call, because it is computed from _func.
    return hash((self._func, self.__name__, self.identity,
                 self.nin, self.nout, self.nargs))
