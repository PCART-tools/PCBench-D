  def __eq__(self, other: Any) -> bool:
    # Do not include _call, because it is computed from _func.
    return isinstance(other, ufunc) and (
      (self._func, self.__name__, self.identity, self.nin, self.nout, self.nargs) ==
      (other._func, other.__name__, other.identity, other.nin, other.nout, other.nargs))
