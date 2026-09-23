  def __oct__(self):
    core.check_integer_conversion(self)
    return oct(self._value)  # type: ignore
