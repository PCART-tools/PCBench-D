  @property
  def value(self) -> _T:
    val = _thread_local_state.__dict__.get(self._name, unset)
    return cast(_T, val) if val is not unset else self._value
