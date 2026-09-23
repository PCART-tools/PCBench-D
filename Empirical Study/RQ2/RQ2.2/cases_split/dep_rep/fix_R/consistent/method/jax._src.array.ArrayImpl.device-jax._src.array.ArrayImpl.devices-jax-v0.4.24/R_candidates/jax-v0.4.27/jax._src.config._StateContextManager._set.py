  def _set(self, value: _T) -> None:
    self._value = value
    if self._update_global_hook:
      self._update_global_hook(value)
