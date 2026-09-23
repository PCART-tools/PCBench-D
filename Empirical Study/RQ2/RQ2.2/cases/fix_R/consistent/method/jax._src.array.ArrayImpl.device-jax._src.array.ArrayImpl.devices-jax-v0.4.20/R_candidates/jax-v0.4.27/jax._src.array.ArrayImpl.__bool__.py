  def __bool__(self):
    core.check_bool_conversion(self)
    return bool(self._value)
