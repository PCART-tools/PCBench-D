  @property
  def device_buffer(self):
    raise AttributeError(
      "arr.device_buffer has been deprecated. Use arr.addressable_data(0)")
