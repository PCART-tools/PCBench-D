  def __reduce__(self):
    return (type(self), (self.devices, self.axis_names))
