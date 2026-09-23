  def __complex__(self):
    check_scalar_conversion(self)
    return self.aval._complex(self)
