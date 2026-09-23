  def __complex__(self):
    core.check_scalar_conversion(self)
    return self._value.__complex__()
