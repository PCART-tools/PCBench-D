  def __float__(self):
    check_scalar_conversion(self)
    return self.aval._float(self)
