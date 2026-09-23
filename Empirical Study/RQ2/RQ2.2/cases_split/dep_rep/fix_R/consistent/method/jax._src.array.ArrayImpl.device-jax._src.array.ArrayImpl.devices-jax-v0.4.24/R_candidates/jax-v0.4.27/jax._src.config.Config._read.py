  def _read(self, name):
    try:
      return self._value_holders[name].value
    except KeyError:
      raise AttributeError(f"Unrecognized config option: {name}")
