  def __int__(self):
    core.check_scalar_conversion(self)
    return self._value.__int__()
