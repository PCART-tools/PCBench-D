  def __oct__(self):
    check_integer_conversion(self)
    return self.aval._oct(self)
