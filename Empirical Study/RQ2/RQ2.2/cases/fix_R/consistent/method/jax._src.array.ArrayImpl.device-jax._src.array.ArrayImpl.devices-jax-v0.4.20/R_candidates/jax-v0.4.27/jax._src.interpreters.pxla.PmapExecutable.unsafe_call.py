  @property
  def unsafe_call(self) -> Callable[..., Any]:
    if self._unsafe_call is None:
      self._unsafe_call = self.build_unsafe_call()
    return self._unsafe_call
