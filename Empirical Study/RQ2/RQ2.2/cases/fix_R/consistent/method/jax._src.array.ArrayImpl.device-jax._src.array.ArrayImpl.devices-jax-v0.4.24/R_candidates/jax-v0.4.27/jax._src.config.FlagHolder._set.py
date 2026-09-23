  def _set(self, value: _T) -> None:
    self.value = value
    if self._update_hook is not None:
      self._update_hook(value)
