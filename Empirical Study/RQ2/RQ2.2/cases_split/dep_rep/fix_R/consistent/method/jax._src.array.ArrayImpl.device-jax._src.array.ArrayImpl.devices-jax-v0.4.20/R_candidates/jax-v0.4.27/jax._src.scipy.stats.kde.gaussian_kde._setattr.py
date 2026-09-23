  def _setattr(self, name, value):
    # Frozen dataclasses don't support setting attributes so we have to
    # overload that operation here as they do in the dataclass implementation
    object.__setattr__(self, name, value)
    return value
