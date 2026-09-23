  @property
  def shape(self):
    return collections.OrderedDict(
        (name, size)
        for name, size in util.safe_zip(self.axis_names, self.devices.shape))
