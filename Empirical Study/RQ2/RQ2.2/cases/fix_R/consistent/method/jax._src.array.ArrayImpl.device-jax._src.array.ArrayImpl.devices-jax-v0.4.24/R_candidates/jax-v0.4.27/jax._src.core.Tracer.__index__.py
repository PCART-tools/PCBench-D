  def __index__(self):
    check_integer_conversion(self)
    raise self.aval._index(self)
