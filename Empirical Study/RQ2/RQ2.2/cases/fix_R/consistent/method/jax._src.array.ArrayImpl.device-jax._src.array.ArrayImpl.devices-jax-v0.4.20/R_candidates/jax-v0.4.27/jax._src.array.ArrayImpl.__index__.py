  def __index__(self):
    core.check_integer_conversion(self)
    return op.index(self._value)
