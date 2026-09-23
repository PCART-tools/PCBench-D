  def __eq__(self, other):
    if not isinstance(other, DeviceLocalLayout):
      return False
    return self._layout == other._layout
