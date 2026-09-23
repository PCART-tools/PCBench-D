  def __float__(self):
    core.check_scalar_conversion(self)
    return self._value.__float__()
