  def __call__(self, axis_name):
    self.axis_names.add(axis_name)
    return (axis_name,)
