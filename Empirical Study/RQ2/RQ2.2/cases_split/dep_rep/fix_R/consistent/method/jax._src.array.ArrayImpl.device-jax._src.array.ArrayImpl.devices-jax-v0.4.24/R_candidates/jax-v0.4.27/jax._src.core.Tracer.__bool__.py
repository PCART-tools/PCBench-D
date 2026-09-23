  def __bool__(self):
    check_bool_conversion(self)
    return self.aval._bool(self)
