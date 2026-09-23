  def __int__(self):
    check_scalar_conversion(self)
    return self.aval._int(self)
