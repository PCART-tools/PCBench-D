  def update(self, name, val):
    if name not in self._value_holders:
      raise AttributeError(f"Unrecognized config option: {name}")
    self._value_holders[name]._set(val)
