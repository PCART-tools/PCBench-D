  def __hex__(self):
    core.check_integer_conversion(self)
    return hex(self._value)  # type: ignore
