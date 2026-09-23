  def __hex__(self):
    check_integer_conversion(self)
    return self.aval._hex(self)
